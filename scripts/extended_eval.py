"""Extended evaluation runner for EXTENDED_EVAL_V1.json (and future versions).

Runs each prompt through the real TaskService pipeline and scores it
against the manifest's expected fields. Produces a markdown report with
per-case detail plus aggregated metrics by category and difficulty.

Scoring (see evidence/materials/EXTENDED_EVAL_SCOPE.md for full spec):
- Answerable cases pass when:
    * cited pages intersect expected_pages (or expected_pages is empty),
    * evidence_mode == "declared",
    * result contains any substring from expected_any_of (case-insensitive).
- Refusal cases pass when retrieval_status == "no_match" or outcome == "refused".

Zero-arg run:
    .venv/Scripts/python.exe scripts/extended_eval.py
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass, field, replace
from datetime import datetime
from pathlib import Path
from statistics import mean

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.core.config import Settings, get_settings
from backend.app.services.auth_service import AuthService
from backend.app.services.file_service import FileService
from backend.app.services.log_service import LogService
from backend.app.services.model_client import ModelClient
from backend.app.services.task_service import TaskService


@dataclass
class EvalCase:
    case_id: str
    doc_id: str
    document_path: str
    language: str
    text: str
    category: str
    kind: str
    expected_pages: list[int]
    expected_any_of: list[str]
    difficulty: str


@dataclass
class EvalRecord:
    case: EvalCase
    success: bool
    outcome: str | None = None
    retrieval_status: str | None = None
    evidence_mode: str | None = None
    cited_pages: list[int] = field(default_factory=list)
    citation_count: int = 0
    evidence_quote_count: int = 0
    latency_ms: int | None = None
    answer_snippet: str = ""
    error: str | None = None
    page_hit: bool = False
    declared: bool = False
    snippet_hit: bool = False
    refusal_hit: bool = False
    passed: bool = False
    fail_reason: str = ""
    failure_type: str = ""
    failure_stage: str = ""


def load_cases(manifest_path: Path) -> list[EvalCase]:
    raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    cases: list[EvalCase] = []
    for item in raw.get("items") or []:
        doc_id = str(item["doc_id"])
        document_path = str(item["document_path"])
        language = str(item.get("language") or "zh")
        for prompt in item.get("prompts") or []:
            cases.append(
                EvalCase(
                    case_id=f"{doc_id}:{prompt['id']}",
                    doc_id=doc_id,
                    document_path=document_path,
                    language=language,
                    text=str(prompt["text"]),
                    category=str(prompt.get("category") or "UNSPEC"),
                    kind=str(prompt.get("kind") or "answerable"),
                    expected_pages=[int(p) for p in prompt.get("expected_pages") or []],
                    expected_any_of=[str(s) for s in prompt.get("expected_any_of") or []],
                    difficulty=str(prompt.get("difficulty") or "medium"),
                )
            )
    return cases


def score(record: EvalRecord) -> None:
    case = record.case
    if case.kind == "refusal":
        record.refusal_hit = (
            record.retrieval_status == "no_match" or record.outcome == "refused"
        )
        record.passed = record.refusal_hit
        if not record.passed:
            record.fail_reason = (
                f"expected refusal but outcome={record.outcome} "
                f"retrieval_status={record.retrieval_status}"
            )
        classify_failure(record)
        return

    if case.expected_pages:
        record.page_hit = bool(set(record.cited_pages) & set(case.expected_pages))
    else:
        record.page_hit = True

    record.declared = record.evidence_mode == "declared"

    lowered = record.answer_snippet.lower()
    if case.expected_any_of:
        record.snippet_hit = any(s.lower() in lowered for s in case.expected_any_of)
    else:
        record.snippet_hit = True

    record.passed = record.page_hit and record.declared and record.snippet_hit
    if not record.passed:
        reasons = []
        if not record.page_hit:
            reasons.append(f"pages {record.cited_pages} ∩ {case.expected_pages} empty")
        if not record.declared:
            reasons.append(f"evidence_mode={record.evidence_mode}")
        if not record.snippet_hit:
            reasons.append(f"answer missing any of {case.expected_any_of}")
        record.fail_reason = "; ".join(reasons)
    classify_failure(record)


def classify_failure(record: EvalRecord) -> None:
    if record.passed:
        record.failure_type = ""
        record.failure_stage = ""
        return

    if record.error:
        record.failure_type = "runtime_error"
        record.failure_stage = "runtime"
        return

    if record.case.kind == "refusal":
        if record.outcome != "refused" and record.retrieval_status != "no_match":
            record.failure_type = "refusal_escape"
            record.failure_stage = "safety_gate"
            return
        record.failure_type = "refusal_mismatch"
        record.failure_stage = "safety_gate"
        return

    if record.retrieval_status == "no_match":
        record.failure_type = "retrieval_miss"
        record.failure_stage = "retrieval"
        return

    if record.retrieval_status == "low_confidence":
        record.failure_type = "low_confidence"
        record.failure_stage = "retrieval"
        return

    if record.outcome == "refused":
        if record.retrieval_status == "matched" and not record.declared:
            record.failure_type = "model_refused_after_retrieval"
            record.failure_stage = "model"
            return
        record.failure_type = "unexpected_refusal"
        record.failure_stage = "model"
        return

    if not record.page_hit and record.citation_count == 0:
        record.failure_type = "missing_citation"
        record.failure_stage = "citation"
        return

    if not record.page_hit:
        record.failure_type = "wrong_page"
        record.failure_stage = "citation"
        return

    if not record.declared:
        record.failure_type = "undeclared_evidence"
        record.failure_stage = "evidence"
        return

    if record.declared and record.evidence_quote_count == 0:
        record.failure_type = "missing_evidence_quote"
        record.failure_stage = "evidence"
        return

    if not record.snippet_hit:
        record.failure_type = "answer_missing_expected_term"
        record.failure_stage = "answer"
        return

    record.failure_type = "unknown_failure"
    record.failure_stage = "unknown"


def build_eval_settings(base_settings: Settings, *, model_name: str | None = None) -> Settings:
    if not model_name:
        return base_settings
    return replace(base_settings, model_qa=model_name)


def run_cases(
    cases: list[EvalCase], *, clear_cache: bool = True, model_name: str | None = None
) -> list[EvalRecord]:
    settings = build_eval_settings(get_settings(), model_name=model_name)
    auth_service = AuthService(settings=settings)
    file_service = FileService(settings=settings)
    log_service = LogService(settings=settings)
    model_client = ModelClient(settings=settings)
    task_service = TaskService(
        file_service=file_service,
        model_client=model_client,
        log_service=log_service,
    )
    session = auth_service.create_session("alpha-demo")
    session_id = session.session.session_id

    uploads: dict[str, object] = {}
    records: list[EvalRecord] = []

    if clear_cache and settings.cache_dir.exists():
        shutil.rmtree(settings.cache_dir, ignore_errors=True)
        settings.cache_dir.mkdir(parents=True, exist_ok=True)
        (settings.cache_dir / ".gitkeep").write_text("", encoding="utf-8")

    for idx, case in enumerate(cases, 1):
        print(f"[{idx}/{len(cases)}] {case.case_id} ({case.category}/{case.difficulty})")
        sample_path = PROJECT_ROOT / case.document_path
        upload = uploads.get(case.document_path)
        if upload is None:
            upload = file_service.save_upload(
                sample_path.name,
                sample_path.read_bytes(),
                owner_session_id=session_id,
            )
            uploads[case.document_path] = upload

        record = EvalRecord(case=case, success=False)
        try:
            result = task_service.run_task(
                task_type="ask",
                endpoint="/api/ask",
                file_id=upload.file_id,
                session_id=session_id,
                document_access_token=upload.access_token,
                user_input=case.text,
                response_detail_level="balanced",
            )
            cited_pages = sorted(
                {p for c in result.citations for p in c.page_numbers}
            )
            record.success = True
            record.outcome = result.outcome
            record.retrieval_status = result.retrieval_status
            record.evidence_mode = result.evidence_mode
            record.cited_pages = cited_pages
            record.citation_count = len(result.citations)
            record.evidence_quote_count = len(result.evidence_quotes)
            record.latency_ms = result.latency_ms
            record.answer_snippet = (result.result or "")[:400]
        except Exception as exc:
            record.error = f"{type(exc).__name__}: {exc}"

        score(record)
        records.append(record)

    return records


def aggregate(records: list[EvalRecord]) -> dict:
    total = len(records)
    passed = sum(1 for r in records if r.passed)
    by_category: dict[str, dict] = {}
    by_difficulty: dict[str, dict] = {}
    by_doc: dict[str, dict] = {}
    by_failure_type: dict[str, int] = {}
    by_failure_stage: dict[str, int] = {}

    def _bucket() -> dict:
        return {"total": 0, "passed": 0, "latency": []}

    answerable = [r for r in records if r.case.kind == "answerable"]
    refusal = [r for r in records if r.case.kind == "refusal"]

    for r in records:
        if not r.passed:
            by_failure_type[r.failure_type or "unknown_failure"] = (
                by_failure_type.get(r.failure_type or "unknown_failure", 0) + 1
            )
            by_failure_stage[r.failure_stage or "unknown"] = (
                by_failure_stage.get(r.failure_stage or "unknown", 0) + 1
            )

        for bucket_map, key in (
            (by_category, r.case.category),
            (by_difficulty, r.case.difficulty),
            (by_doc, r.case.doc_id),
        ):
            b = bucket_map.setdefault(key, _bucket())
            b["total"] += 1
            if r.passed:
                b["passed"] += 1
            if r.latency_ms is not None:
                b["latency"].append(r.latency_ms)

    for bucket_map in (by_category, by_difficulty, by_doc):
        for b in bucket_map.values():
            b["pass_rate"] = b["passed"] / b["total"] if b["total"] else 0.0
            b["avg_latency_ms"] = int(mean(b["latency"])) if b["latency"] else 0
            del b["latency"]

    return {
        "total": total,
        "passed": passed,
        "overall_pass_rate": passed / total if total else 0.0,
        "answerable_pass_rate": (
            sum(1 for r in answerable if r.passed) / len(answerable) if answerable else 0.0
        ),
        "refusal_precision": (
            sum(1 for r in refusal if r.passed) / len(refusal) if refusal else 0.0
        ),
        "citation_accuracy": (
            sum(1 for r in answerable if r.page_hit) / len(answerable) if answerable else 0.0
        ),
        "declaration_rate": (
            sum(1 for r in answerable if r.declared) / len(answerable) if answerable else 0.0
        ),
        "avg_latency_ms": (
            int(mean([r.latency_ms for r in records if r.latency_ms is not None]))
            if any(r.latency_ms for r in records)
            else 0
        ),
        "by_category": by_category,
        "by_difficulty": by_difficulty,
        "by_doc": by_doc,
        "by_failure_type": by_failure_type,
        "by_failure_stage": by_failure_stage,
    }


def render_markdown(records: list[EvalRecord], summary: dict, manifest_name: str) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# Extended Evaluation Report — {manifest_name}",
        "",
        f"Generated: {now}",
        "",
        "## Overall",
        "",
        f"- Total cases: **{summary['total']}**",
        f"- Passed: **{summary['passed']}**",
        f"- Overall pass rate: **{summary['overall_pass_rate']*100:.1f}%**",
        f"- Answerable pass rate: **{summary['answerable_pass_rate']*100:.1f}%**",
        f"- Refusal precision: **{summary['refusal_precision']*100:.1f}%**",
        f"- Citation accuracy (answerable page-hit): **{summary['citation_accuracy']*100:.1f}%**",
        f"- Declaration rate (evidence_mode=declared on answerable): **{summary['declaration_rate']*100:.1f}%**",
        f"- Avg latency: **{summary['avg_latency_ms']} ms**",
        "",
        "## By Category",
        "",
        "| Category | Total | Passed | Pass rate | Avg latency (ms) |",
        "| --- | --- | --- | --- | --- |",
    ]
    for cat, b in sorted(summary["by_category"].items()):
        lines.append(
            f"| {cat} | {b['total']} | {b['passed']} | {b['pass_rate']*100:.1f}% | {b['avg_latency_ms']} |"
        )
    lines.extend([
        "",
        "## By Difficulty",
        "",
        "| Difficulty | Total | Passed | Pass rate | Avg latency (ms) |",
        "| --- | --- | --- | --- | --- |",
    ])
    for diff, b in sorted(summary["by_difficulty"].items()):
        lines.append(
            f"| {diff} | {b['total']} | {b['passed']} | {b['pass_rate']*100:.1f}% | {b['avg_latency_ms']} |"
        )
    lines.extend([
        "",
        "## By Document",
        "",
        "| Doc | Total | Passed | Pass rate | Avg latency (ms) |",
        "| --- | --- | --- | --- | --- |",
    ])
    for doc, b in sorted(summary["by_doc"].items()):
        lines.append(
            f"| {doc} | {b['total']} | {b['passed']} | {b['pass_rate']*100:.1f}% | {b['avg_latency_ms']} |"
        )

    failed_records = [record for record in records if not record.passed]
    lines.extend([
        "",
        "## Failure Attribution",
        "",
        "| Failure type | Count |",
        "| --- | ---: |",
    ])
    if summary["by_failure_type"]:
        for failure_type, count in sorted(
            summary["by_failure_type"].items(), key=lambda item: (-item[1], item[0])
        ):
            lines.append(f"| {failure_type} | {count} |")
    else:
        lines.append("| (none) | 0 |")

    lines.extend([
        "",
        "| Failure stage | Count |",
        "| --- | ---: |",
    ])
    if summary["by_failure_stage"]:
        for failure_stage, count in sorted(
            summary["by_failure_stage"].items(), key=lambda item: (-item[1], item[0])
        ):
            lines.append(f"| {failure_stage} | {count} |")
    else:
        lines.append("| (none) | 0 |")

    lines.extend(["", "### Failed Case Triage", ""])
    if failed_records:
        lines.extend([
            "| Case | Failure type | Stage | Reason |",
            "| --- | --- | --- | --- |",
        ])
        for record in failed_records:
            reason = (record.fail_reason or record.error or "").replace("|", "\\|")
            lines.append(
                f"| {record.case.case_id} | {record.failure_type} | {record.failure_stage} | {reason} |"
            )
    else:
        lines.append("No failed cases.")

    lines.extend(["", "## Case Detail", ""])
    for r in records:
        status = "PASS" if r.passed else "FAIL"
        lines.extend([
            f"### [{status}] {r.case.case_id}",
            f"- Category: {r.case.category} / Difficulty: {r.case.difficulty} / Kind: {r.case.kind}",
            f"- Query: {r.case.text}",
            f"- Expected pages: {r.case.expected_pages} | Expected any of: {r.case.expected_any_of}",
            f"- Outcome: {r.outcome} | retrieval_status: {r.retrieval_status} | evidence_mode: {r.evidence_mode}",
            f"- Cited pages: {r.cited_pages} | citations: {r.citation_count} | evidence_quotes: {r.evidence_quote_count}",
            f"- Latency: {r.latency_ms} ms",
            f"- Fail reason: {r.fail_reason}" if r.fail_reason else "- Fail reason: (none)",
            f"- Failure type: {r.failure_type or '(none)'} | stage: {r.failure_stage or '(none)'}",
            f"- Answer snippet: {r.answer_snippet[:200]}",
            f"- Error: {r.error}" if r.error else "- Error: (none)",
            "",
        ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=str,
        default="evidence/materials/EXTENDED_EVAL_V1.json",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="evidence/reports/extended_eval_v1_latest.md",
    )
    parser.add_argument(
        "--json-output",
        type=str,
        default="evidence/reports/extended_eval_v1_latest.json",
    )
    parser.add_argument("--no-clear-cache", action="store_true")
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Override MODEL_QA for this run without editing .env.",
    )
    args = parser.parse_args()

    manifest_path = PROJECT_ROOT / args.manifest
    cases = load_cases(manifest_path)
    if not cases:
        print("No cases found in manifest.")
        sys.exit(1)
    print(f"Loaded {len(cases)} cases from {manifest_path}")

    if args.model:
        print(f"Using QA model override: {args.model}")

    records = run_cases(cases, clear_cache=not args.no_clear_cache, model_name=args.model)
    summary = aggregate(records)

    output_path = PROJECT_ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_markdown(records, summary, manifest_path.stem),
        encoding="utf-8",
    )

    json_path = PROJECT_ROOT / args.json_output
    json_path.write_text(
        json.dumps(
            {
                "summary": summary,
                "records": [
                    {
                        "case_id": r.case.case_id,
                        "category": r.case.category,
                        "difficulty": r.case.difficulty,
                        "kind": r.case.kind,
                        "passed": r.passed,
                        "fail_reason": r.fail_reason,
                        "failure_type": r.failure_type,
                        "failure_stage": r.failure_stage,
                        "page_hit": r.page_hit,
                        "declared": r.declared,
                        "snippet_hit": r.snippet_hit,
                        "outcome": r.outcome,
                        "retrieval_status": r.retrieval_status,
                        "evidence_mode": r.evidence_mode,
                        "cited_pages": r.cited_pages,
                        "citation_count": r.citation_count,
                        "evidence_quote_count": r.evidence_quote_count,
                        "latency_ms": r.latency_ms,
                        "error": r.error,
                    }
                    for r in records
                ],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"\nReport written to {output_path}")
    print(f"Summary JSON written to {json_path}")
    print(
        f"Overall: {summary['passed']}/{summary['total']} "
        f"({summary['overall_pass_rate']*100:.1f}%), "
        f"refusal precision {summary['refusal_precision']*100:.1f}%, "
        f"citation accuracy {summary['citation_accuracy']*100:.1f}%"
    )


if __name__ == "__main__":
    main()
