from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from statistics import mean

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.core.config import get_settings
from backend.app.services.auth_service import AuthService
from backend.app.services.file_service import FileService
from backend.app.services.log_service import LogService
from backend.app.services.model_client import ModelClient
from backend.app.services.task_service import TaskService


@dataclass
class ReplayRecord:
    sample_id: str
    scenario: str
    file_path: str
    task_type: str
    input_text: str
    response_detail_level: str | None
    success: bool
    outcome: str | None
    latency_ms: int | None
    model_name: str | None
    route_tier: str | None
    route_model: str | None
    route_reason: str | None
    cache_hit: bool | None
    retrieval_status: str | None
    used_chunk_count: int | None
    evidence_quote_count: int | None
    citation_count: int | None
    source_chunk_count: int | None
    error: str | None


@dataclass
class ReplayTask:
    sample_id: str
    scenario: str
    file_path: str
    task_type: str
    input_text: str
    response_detail_level: str


def render_markdown(records: list[ReplayRecord]) -> str:
    lines = ["# Sample Replay Report", ""]
    for record in records:
        lines.extend(
            [
                f"## {record.sample_id} / {record.task_type}",
                f"- Scenario: {record.scenario}",
                f"- File: {record.file_path}",
                f"- Input: {record.input_text}",
                f"- Response detail level: {record.response_detail_level}",
                f"- Success: {record.success}",
                f"- Outcome: {record.outcome}",
                f"- Latency (ms): {record.latency_ms}",
                f"- Model: {record.model_name}",
                f"- Route tier: {record.route_tier}",
                f"- Route model: {record.route_model}",
                f"- Route reason: {record.route_reason}",
                f"- Cache hit: {record.cache_hit}",
                f"- Retrieval status: {record.retrieval_status}",
                f"- Used chunk count: {record.used_chunk_count}",
                f"- Evidence quote count: {record.evidence_quote_count}",
                f"- Citation count: {record.citation_count}",
                f"- Source chunk count: {record.source_chunk_count}",
                f"- Error: {record.error}",
                "",
            ]
        )
    return "\n".join(lines)


def summarize_records(records: list[ReplayRecord]) -> dict:
    by_task: dict[str, list[ReplayRecord]] = {}
    by_route_tier: dict[str, list[ReplayRecord]] = {}
    by_outcome: dict[str, int] = {}
    by_detail: dict[str, list[ReplayRecord]] = {}

    for record in records:
        by_task.setdefault(record.task_type, []).append(record)
        by_route_tier.setdefault(record.route_tier or "unknown", []).append(record)
        by_outcome[record.outcome or "unknown"] = by_outcome.get(record.outcome or "unknown", 0) + 1
        by_detail.setdefault(record.response_detail_level or "unknown", []).append(record)

    def _task_summary(items: list[ReplayRecord]) -> dict:
        latencies = [item.latency_ms for item in items if item.latency_ms is not None]
        return {
            "count": len(items),
            "average_latency_ms": int(mean(latencies)) if latencies else 0,
            "answered": sum(1 for item in items if item.outcome == "answered"),
            "refused": sum(1 for item in items if item.outcome == "refused"),
            "errors": sum(1 for item in items if item.success is False),
            "used_chunk_count_sum": sum(item.used_chunk_count or 0 for item in items),
            "evidence_quote_count_sum": sum(item.evidence_quote_count or 0 for item in items),
        }

    return {
        "total_records": len(records),
        "by_task": {task: _task_summary(items) for task, items in by_task.items()},
        "by_route_tier": {tier: _task_summary(items) for tier, items in by_route_tier.items()},
        "by_outcome": by_outcome,
        "by_response_detail_level": {
            level: _task_summary(items) for level, items in by_detail.items()
        },
    }


def render_summary_markdown(summary: dict) -> str:
    lines = [
        "# Sample Replay Summary",
        "",
        f"- Total records: {summary['total_records']}",
        "",
        "## By Task",
    ]
    for task, item in summary["by_task"].items():
        lines.extend(
            [
                f"### {task}",
                f"- Count: {item['count']}",
                f"- Average latency (ms): {item['average_latency_ms']}",
                f"- Answered: {item['answered']}",
                f"- Refused: {item['refused']}",
                f"- Errors: {item['errors']}",
                f"- Used chunk count sum: {item['used_chunk_count_sum']}",
                f"- Evidence quote count sum: {item['evidence_quote_count_sum']}",
                "",
            ]
        )

    lines.append("## By Route Tier")
    for tier, item in summary["by_route_tier"].items():
        lines.extend(
            [
                f"### {tier}",
                f"- Count: {item['count']}",
                f"- Average latency (ms): {item['average_latency_ms']}",
                f"- Answered: {item['answered']}",
                f"- Refused: {item['refused']}",
                f"- Errors: {item['errors']}",
                f"- Used chunk count sum: {item['used_chunk_count_sum']}",
                f"- Evidence quote count sum: {item['evidence_quote_count_sum']}",
                "",
            ]
        )

    lines.append("## By Response Detail Level")
    for level, item in summary["by_response_detail_level"].items():
        lines.extend(
            [
                f"### {level}",
                f"- Count: {item['count']}",
                f"- Average latency (ms): {item['average_latency_ms']}",
                f"- Answered: {item['answered']}",
                f"- Refused: {item['refused']}",
                f"- Errors: {item['errors']}",
                f"- Used chunk count sum: {item['used_chunk_count_sum']}",
                f"- Evidence quote count sum: {item['evidence_quote_count_sum']}",
                "",
            ]
        )

    lines.append("## By Outcome")
    for outcome, count in summary["by_outcome"].items():
        lines.append(f"- {outcome}: {count}")

    return "\n".join(lines) + "\n"


def normalize_manifest(raw_manifest: object) -> list[ReplayTask]:
    tasks: list[ReplayTask] = []

    if isinstance(raw_manifest, list):
        for item in raw_manifest:
            if not isinstance(item, dict):
                continue
            response_detail_level = str(item.get("response_detail_level") or "balanced")
            item_id = str(item["id"])
            scenario = str(item.get("scenario") or item_id)
            file_path = str(item["path"])
            for task_type, prompt in (item.get("tasks") or {}).items():
                tasks.append(
                    ReplayTask(
                        sample_id=item_id,
                        scenario=scenario,
                        file_path=file_path,
                        task_type=str(task_type),
                        input_text=str(prompt),
                        response_detail_level=response_detail_level,
                    )
                )
        return tasks

    if isinstance(raw_manifest, dict) and "prompts" in raw_manifest:
        response_detail_level = str(raw_manifest.get("response_detail_level") or "balanced")
        item_id = str(raw_manifest.get("id") or "manifest")
        scenario = str(raw_manifest.get("scenario") or item_id)
        file_path = str(raw_manifest["document_path"])
        for prompt in raw_manifest.get("prompts") or []:
            if not isinstance(prompt, dict):
                continue
            tasks.append(
                ReplayTask(
                    sample_id=f"{item_id}:{prompt['id']}",
                    scenario=scenario,
                    file_path=file_path,
                    task_type="ask",
                    input_text=str(prompt["text"]),
                    response_detail_level=response_detail_level,
                )
            )
        return tasks

    raise ValueError("Unsupported manifest format.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay fixed sample set against current services.")
    parser.add_argument(
        "--manifest",
        type=str,
        default="evidence/materials/SAMPLE_MANIFEST.json",
        help="Path to sample manifest JSON.",
    )
    parser.add_argument(
        "--format",
        choices=["json", "md"],
        default="md",
        help="Output report format.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Optional output file path.",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Force mock model mode for dry replay.",
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear local cache before replay so the report reflects fresh runs.",
    )
    parser.add_argument(
        "--timestamped",
        action="store_true",
        help="If output is provided, append a timestamp to the output filename.",
    )
    parser.add_argument(
        "--summary-output",
        type=str,
        default=None,
        help="Optional output file path for the aggregated replay summary.",
    )
    parser.add_argument(
        "--invite-code",
        type=str,
        default="alpha-demo",
        help="Invite code used to create the controlled-alpha replay session.",
    )
    args = parser.parse_args()

    if args.mock:
        os.environ["USE_MOCK_MODEL"] = "true"
        os.environ["MODEL_PROVIDER"] = "mock"
        get_settings.cache_clear()

    settings = get_settings()
    auth_service = AuthService(settings=settings)
    file_service = FileService(settings=settings)
    log_service = LogService(settings=settings)
    model_client = ModelClient(settings=settings)
    task_service = TaskService(
        file_service=file_service,
        model_client=model_client,
        log_service=log_service,
    )

    manifest_path = PROJECT_ROOT / args.manifest
    raw_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    replay_tasks = normalize_manifest(raw_manifest)

    session = auth_service.create_session(args.invite_code)
    session_id = session.session.session_id

    records: list[ReplayRecord] = []
    uploads_by_path: dict[str, object] = {}

    for replay_task in replay_tasks:
        sample_path = PROJECT_ROOT / replay_task.file_path
        content = sample_path.read_bytes()
        upload = uploads_by_path.get(replay_task.file_path)
        if upload is None:
            upload = file_service.save_upload(
                sample_path.name,
                content,
                owner_session_id=session_id,
            )
            uploads_by_path[replay_task.file_path] = upload

        try:
            if args.clear_cache and settings.cache_dir.exists():
                shutil.rmtree(settings.cache_dir, ignore_errors=True)
                settings.cache_dir.mkdir(parents=True, exist_ok=True)
                (settings.cache_dir / ".gitkeep").write_text("", encoding="utf-8")
            result = task_service.run_task(
                task_type=replay_task.task_type,
                endpoint=f"/api/{replay_task.task_type}",
                file_id=upload.file_id,
                session_id=session_id,
                document_access_token=upload.access_token,
                user_input=replay_task.input_text,
                response_detail_level=replay_task.response_detail_level,
            )
            records.append(
                ReplayRecord(
                    sample_id=replay_task.sample_id,
                    scenario=replay_task.scenario,
                    file_path=replay_task.file_path,
                    task_type=replay_task.task_type,
                    input_text=replay_task.input_text,
                    response_detail_level=result.response_detail_level,
                    success=True,
                    outcome=result.outcome,
                    latency_ms=result.latency_ms,
                    model_name=result.model_name,
                    route_tier=result.route_tier,
                    route_model=result.route_model,
                    route_reason=result.route_reason,
                    cache_hit=result.cache_hit,
                    retrieval_status=result.retrieval_status,
                    used_chunk_count=len(result.used_chunk_ids),
                    evidence_quote_count=len(result.evidence_quotes),
                    citation_count=len(result.citations),
                    source_chunk_count=len(result.source_chunks),
                    error=None,
                )
            )
        except Exception as exc:  # pragma: no cover
            records.append(
                ReplayRecord(
                    sample_id=replay_task.sample_id,
                    scenario=replay_task.scenario,
                    file_path=replay_task.file_path,
                    task_type=replay_task.task_type,
                    input_text=replay_task.input_text,
                    response_detail_level=replay_task.response_detail_level,
                    success=False,
                    outcome="error",
                    latency_ms=None,
                    model_name=None,
                    route_tier=None,
                    route_model=None,
                    route_reason=None,
                    cache_hit=None,
                    retrieval_status=None,
                    used_chunk_count=None,
                    evidence_quote_count=None,
                    citation_count=None,
                    source_chunk_count=None,
                    error=str(exc),
                )
            )

    rendered = (
        json.dumps([asdict(record) for record in records], ensure_ascii=False, indent=2)
        if args.format == "json"
        else render_markdown(records)
    )
    summary = summarize_records(records)
    summary_rendered = (
        json.dumps(summary, ensure_ascii=False, indent=2)
        if args.format == "json"
        else render_summary_markdown(summary)
    )

    if args.output:
        output_path = Path(args.output)
        if args.timestamped:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = output_path.with_name(
                f"{output_path.stem}_{timestamp}{output_path.suffix}"
            )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
        print(f"Saved replay report to {output_path}")
    if args.summary_output:
        summary_output_path = Path(args.summary_output)
        if args.timestamped:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            summary_output_path = summary_output_path.with_name(
                f"{summary_output_path.stem}_{timestamp}{summary_output_path.suffix}"
            )
        summary_output_path.parent.mkdir(parents=True, exist_ok=True)
        summary_output_path.write_text(summary_rendered, encoding="utf-8")
        print(f"Saved replay summary to {summary_output_path}")
        if args.output:
            return

    if args.output:
        return

    print(rendered)


if __name__ == "__main__":
    main()
