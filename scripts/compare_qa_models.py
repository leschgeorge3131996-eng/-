from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from statistics import mean
from typing import Literal

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.core.config import Settings, get_settings
from backend.app.services.auth_service import AuthService
from backend.app.services.file_service import FileService
from backend.app.services.log_service import LogService
from backend.app.services.model_client import ModelClient
from backend.app.services.task_service import TaskService

PromptKind = Literal["answerable", "refusal"]


@dataclass
class PromptRecord:
    model_name: str
    prompt_id: str
    prompt_kind: PromptKind
    prompt_text: str
    success: bool
    passed: bool
    outcome: str | None
    latency_ms: int | None
    route_tier: str | None
    route_reason: str | None
    cache_hit: bool | None
    retrieval_status: str | None
    citation_count: int | None
    cited_pages: list[int]
    page_fetch_ok: bool | None
    render_ok: bool | None
    evidence_quote_count: int | None
    token_total: int | None
    answer_preview: str | None
    error: str | None


@dataclass
class ModelSummary:
    model_name: str
    total_prompts: int
    passed_prompts: int
    answerable_passed: int
    answerable_total: int
    refusal_passed: int
    refusal_total: int
    average_latency_ms: int
    max_latency_ms: int
    all_passed: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare QA models on a fixed gold-sample candidate ask set."
    )
    parser.add_argument(
        "--manifest",
        default="evidence/materials/GOLD_SAMPLE_CANDIDATE_20260418.json",
        help="Path to the gold-sample candidate manifest JSON.",
    )
    parser.add_argument(
        "--models",
        default="qwen3-235b-a22b-instruct-2507,qwen3-32b",
        help="Comma-separated QA model names to compare.",
    )
    parser.add_argument(
        "--output",
        default="evidence/reports/gold_sample_qa_compare_latest.md",
        help="Output report path.",
    )
    parser.add_argument(
        "--json-output",
        default="evidence/reports/gold_sample_qa_compare_latest.json",
        help="Optional JSON output path.",
    )
    parser.add_argument(
        "--clear-workdir",
        action="store_true",
        help="Clear the per-model temporary workspace before running.",
    )
    return parser.parse_args()


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_run_settings(
    base_settings: Settings,
    *,
    model_name: str,
    run_root: Path,
) -> Settings:
    data_dir = run_root / "data"
    settings = replace(
        base_settings,
        data_dir=data_dir,
        uploads_dir=data_dir / "uploads",
        parsed_dir=data_dir / "parsed",
        sessions_dir=data_dir / "sessions",
        logs_dir=data_dir / "logs",
        cache_dir=data_dir / "cache",
        model_qa=model_name,
    )
    settings.ensure_directories()
    return settings


def make_slug(value: str) -> str:
    return "".join(char if char.isalnum() else "_" for char in value).strip("_").lower()


def validate_answerable(
    *,
    success: bool,
    outcome: str | None,
    citation_count: int,
    page_fetch_ok: bool | None,
    render_ok: bool | None,
) -> bool:
    return (
        success
        and outcome == "answered"
        and citation_count > 0
        and page_fetch_ok is True
        and render_ok is True
    )


def validate_refusal(
    *,
    success: bool,
    outcome: str | None,
    retrieval_status: str | None,
    citation_count: int,
) -> bool:
    return (
        success
        and outcome == "refused"
        and retrieval_status == "no_match"
        and citation_count == 0
    )


def run_prompt_set(
    *,
    settings: Settings,
    manifest: dict,
    model_name: str,
    sample_path: Path,
) -> tuple[list[PromptRecord], ModelSummary]:
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
    upload = file_service.save_upload(
        sample_path.name,
        sample_path.read_bytes(),
        owner_session_id=session_id,
    )

    records: list[PromptRecord] = []
    for prompt in manifest["prompts"]:
        prompt_id = str(prompt["id"])
        prompt_kind = str(prompt["kind"])
        prompt_text = str(prompt["text"])
        page_fetch_ok: bool | None = None
        render_ok: bool | None = None
        cited_pages: list[int] = []

        try:
            result = task_service.run_task(
                task_type="ask",
                endpoint="/api/ask",
                file_id=upload.file_id,
                session_id=session_id,
                document_access_token=upload.access_token,
                user_input=prompt_text,
                response_detail_level=manifest.get("response_detail_level", "balanced"),
            )
            cited_pages = sorted(
                {
                    page
                    for citation in result.citations
                    for page in citation.page_numbers
                }
            )
            if cited_pages:
                first_page = cited_pages[0]
                try:
                    file_service.get_document_page(
                        upload.file_id,
                        first_page,
                        access_token=upload.access_token,
                        session_id=session_id,
                    )
                    page_fetch_ok = True
                except Exception:
                    page_fetch_ok = False

                try:
                    png_bytes = file_service.render_document_page(
                        upload.file_id,
                        first_page,
                        access_token=upload.access_token,
                        session_id=session_id,
                        dpi=144,
                    )
                    render_ok = bool(png_bytes)
                except Exception:
                    render_ok = False

            citation_count = len(result.citations)
            success = True
            if prompt_kind == "answerable":
                passed = validate_answerable(
                    success=success,
                    outcome=result.outcome,
                    citation_count=citation_count,
                    page_fetch_ok=page_fetch_ok,
                    render_ok=render_ok,
                )
            else:
                passed = validate_refusal(
                    success=success,
                    outcome=result.outcome,
                    retrieval_status=result.retrieval_status,
                    citation_count=citation_count,
                )

            records.append(
                PromptRecord(
                    model_name=model_name,
                    prompt_id=prompt_id,
                    prompt_kind=prompt_kind,
                    prompt_text=prompt_text,
                    success=success,
                    passed=passed,
                    outcome=result.outcome,
                    latency_ms=result.latency_ms,
                    route_tier=result.route_tier,
                    route_reason=result.route_reason,
                    cache_hit=result.cache_hit,
                    retrieval_status=result.retrieval_status,
                    citation_count=citation_count,
                    cited_pages=cited_pages,
                    page_fetch_ok=page_fetch_ok,
                    render_ok=render_ok,
                    evidence_quote_count=len(result.evidence_quotes),
                    token_total=(
                        result.token_usage.total_tokens if result.token_usage else None
                    ),
                    answer_preview=result.result[:280],
                    error=None,
                )
            )
        except Exception as exc:  # pragma: no cover
            records.append(
                PromptRecord(
                    model_name=model_name,
                    prompt_id=prompt_id,
                    prompt_kind=prompt_kind,  # type: ignore[arg-type]
                    prompt_text=prompt_text,
                    success=False,
                    passed=False,
                    outcome="error",
                    latency_ms=None,
                    route_tier=None,
                    route_reason=None,
                    cache_hit=None,
                    retrieval_status=None,
                    citation_count=None,
                    cited_pages=[],
                    page_fetch_ok=None,
                    render_ok=None,
                    evidence_quote_count=None,
                    token_total=None,
                    answer_preview=None,
                    error=str(exc),
                )
            )

    answerable_records = [record for record in records if record.prompt_kind == "answerable"]
    refusal_records = [record for record in records if record.prompt_kind == "refusal"]
    latencies = [record.latency_ms for record in records if record.latency_ms is not None]

    summary = ModelSummary(
        model_name=model_name,
        total_prompts=len(records),
        passed_prompts=sum(1 for record in records if record.passed),
        answerable_passed=sum(1 for record in answerable_records if record.passed),
        answerable_total=len(answerable_records),
        refusal_passed=sum(1 for record in refusal_records if record.passed),
        refusal_total=len(refusal_records),
        average_latency_ms=int(mean(latencies)) if latencies else 0,
        max_latency_ms=max(latencies) if latencies else 0,
        all_passed=all(record.passed for record in records) if records else False,
    )
    return records, summary


def render_markdown(
    *,
    manifest: dict,
    summaries: list[ModelSummary],
    records: list[PromptRecord],
) -> str:
    lines = [
        "# Gold Sample QA Compare",
        "",
        f"- Candidate ID: {manifest['id']}",
        f"- Scenario: {manifest.get('scenario')}",
        f"- Document: {manifest['document_path']}",
        f"- Response detail level: {manifest.get('response_detail_level', 'balanced')}",
        "",
        "## Candidate Prompts",
    ]
    for prompt in manifest["prompts"]:
        lines.extend(
            [
                f"### {prompt['id']}",
                f"- Kind: {prompt['kind']}",
                f"- Prompt: {prompt['text']}",
                "",
            ]
        )

    lines.append("## Model Summary")
    lines.append("")
    lines.append("| Model | All Passed | Passed / Total | Answerable Passed | Refusal Passed | Avg Latency (ms) | Max Latency (ms) |")
    lines.append("| --- | --- | --- | --- | --- | ---: | ---: |")
    for summary in summaries:
        lines.append(
            "| "
            + " | ".join(
                [
                    summary.model_name,
                    str(summary.all_passed),
                    f"{summary.passed_prompts} / {summary.total_prompts}",
                    f"{summary.answerable_passed} / {summary.answerable_total}",
                    f"{summary.refusal_passed} / {summary.refusal_total}",
                    str(summary.average_latency_ms),
                    str(summary.max_latency_ms),
                ]
            )
            + " |"
        )
    lines.append("")

    lines.append("## Detailed Results")
    for model_name in [summary.model_name for summary in summaries]:
        lines.append("")
        lines.append(f"### {model_name}")
        for record in [item for item in records if item.model_name == model_name]:
            lines.extend(
                [
                    f"#### {record.prompt_id}",
                    f"- Kind: {record.prompt_kind}",
                    f"- Prompt: {record.prompt_text}",
                    f"- Success: {record.success}",
                    f"- Passed: {record.passed}",
                    f"- Outcome: {record.outcome}",
                    f"- Latency (ms): {record.latency_ms}",
                    f"- Route tier: {record.route_tier}",
                    f"- Route reason: {record.route_reason}",
                    f"- Cache hit: {record.cache_hit}",
                    f"- Retrieval status: {record.retrieval_status}",
                    f"- Citation count: {record.citation_count}",
                    f"- Cited pages: {record.cited_pages}",
                    f"- Page fetch OK: {record.page_fetch_ok}",
                    f"- Render OK: {record.render_ok}",
                    f"- Evidence quote count: {record.evidence_quote_count}",
                    f"- Token total: {record.token_total}",
                    f"- Answer preview: {record.answer_preview}",
                    f"- Error: {record.error}",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    base_settings = get_settings()
    manifest_path = PROJECT_ROOT / args.manifest
    manifest = load_manifest(manifest_path)
    sample_path = PROJECT_ROOT / manifest["document_path"]
    models = [item.strip() for item in args.models.split(",") if item.strip()]

    all_records: list[PromptRecord] = []
    summaries: list[ModelSummary] = []
    work_root = PROJECT_ROOT / ".test_tmp" / "qa_model_compare"

    for model_name in models:
        run_root = work_root / make_slug(model_name)
        if args.clear_workdir and run_root.exists():
            shutil.rmtree(run_root)
        settings = build_run_settings(
            base_settings,
            model_name=model_name,
            run_root=run_root,
        )
        records, summary = run_prompt_set(
            settings=settings,
            manifest=manifest,
            model_name=model_name,
            sample_path=sample_path,
        )
        all_records.extend(records)
        summaries.append(summary)

    markdown_output = render_markdown(
        manifest=manifest,
        summaries=summaries,
        records=all_records,
    )
    json_output = json.dumps(
        {
            "manifest": manifest,
            "summaries": [asdict(summary) for summary in summaries],
            "records": [asdict(record) for record in all_records],
        },
        ensure_ascii=False,
        indent=2,
    )

    output_path = PROJECT_ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_output, encoding="utf-8")

    if args.json_output:
        json_output_path = PROJECT_ROOT / args.json_output
        json_output_path.parent.mkdir(parents=True, exist_ok=True)
        json_output_path.write_text(json_output, encoding="utf-8")

    print(f"Saved markdown report to {output_path}")
    if args.json_output:
        print(f"Saved JSON report to {PROJECT_ROOT / args.json_output}")


if __name__ == "__main__":
    main()
