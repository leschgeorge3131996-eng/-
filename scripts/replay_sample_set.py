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
    success: bool
    outcome: str | None
    latency_ms: int | None
    model_name: str | None
    route_tier: str | None
    route_model: str | None
    route_reason: str | None
    cache_hit: bool | None
    retrieval_status: str | None
    citation_count: int | None
    source_chunk_count: int | None
    error: str | None


def render_markdown(records: list[ReplayRecord]) -> str:
    lines = ["# Sample Replay Report", ""]
    for record in records:
        lines.extend(
            [
                f"## {record.sample_id} / {record.task_type}",
                f"- Scenario: {record.scenario}",
                f"- File: {record.file_path}",
                f"- Input: {record.input_text}",
                f"- Success: {record.success}",
                f"- Outcome: {record.outcome}",
                f"- Latency (ms): {record.latency_ms}",
                f"- Model: {record.model_name}",
                f"- Route tier: {record.route_tier}",
                f"- Route model: {record.route_model}",
                f"- Route reason: {record.route_reason}",
                f"- Cache hit: {record.cache_hit}",
                f"- Retrieval status: {record.retrieval_status}",
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

    for record in records:
        by_task.setdefault(record.task_type, []).append(record)
        by_route_tier.setdefault(record.route_tier or "unknown", []).append(record)
        by_outcome[record.outcome or "unknown"] = by_outcome.get(record.outcome or "unknown", 0) + 1

    def _task_summary(items: list[ReplayRecord]) -> dict:
        latencies = [item.latency_ms for item in items if item.latency_ms is not None]
        return {
            "count": len(items),
            "average_latency_ms": int(mean(latencies)) if latencies else 0,
            "answered": sum(1 for item in items if item.outcome == "answered"),
            "refused": sum(1 for item in items if item.outcome == "refused"),
            "errors": sum(1 for item in items if item.success is False),
        }

    return {
        "total_records": len(records),
        "by_task": {task: _task_summary(items) for task, items in by_task.items()},
        "by_route_tier": {tier: _task_summary(items) for tier, items in by_route_tier.items()},
        "by_outcome": by_outcome,
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
                "",
            ]
        )

    lines.append("## By Outcome")
    for outcome, count in summary["by_outcome"].items():
        lines.append(f"- {outcome}: {count}")

    return "\n".join(lines) + "\n"


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
    args = parser.parse_args()

    if args.mock:
        os.environ["USE_MOCK_MODEL"] = "true"
        os.environ["MODEL_PROVIDER"] = "mock"
        get_settings.cache_clear()

    settings = get_settings()
    file_service = FileService(settings=settings)
    log_service = LogService(settings=settings)
    model_client = ModelClient(settings=settings)
    task_service = TaskService(
        file_service=file_service,
        model_client=model_client,
        log_service=log_service,
    )

    manifest_path = PROJECT_ROOT / args.manifest
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    records: list[ReplayRecord] = []
    for item in manifest:
        sample_path = PROJECT_ROOT / item["path"]
        content = sample_path.read_bytes()
        upload = file_service.save_upload(sample_path.name, content)

        for task_type, prompt in item["tasks"].items():
            try:
                if args.clear_cache and settings.cache_dir.exists():
                    shutil.rmtree(settings.cache_dir, ignore_errors=True)
                    settings.cache_dir.mkdir(parents=True, exist_ok=True)
                    (settings.cache_dir / ".gitkeep").write_text("", encoding="utf-8")
                result = task_service.run_task(
                    task_type=task_type,
                    endpoint=f"/api/{task_type}",
                    file_id=upload.file_id,
                    user_input=prompt,
                )
                records.append(
                    ReplayRecord(
                        sample_id=item["id"],
                        scenario=item["scenario"],
                        file_path=item["path"],
                        task_type=task_type,
                        input_text=prompt,
                        success=True,
                        outcome=result.outcome,
                        latency_ms=result.latency_ms,
                        model_name=result.model_name,
                        route_tier=result.route_tier,
                        route_model=result.route_model,
                        route_reason=result.route_reason,
                        cache_hit=result.cache_hit,
                        retrieval_status=result.retrieval_status,
                        citation_count=len(result.citations),
                        source_chunk_count=len(result.source_chunks),
                        error=None,
                    )
                )
            except Exception as exc:  # pragma: no cover
                records.append(
                    ReplayRecord(
                        sample_id=item["id"],
                        scenario=item["scenario"],
                        file_path=item["path"],
                        task_type=task_type,
                        input_text=prompt,
                        success=False,
                        outcome=None,
                        latency_ms=None,
                        model_name=None,
                        route_tier=None,
                        route_model=None,
                        route_reason=None,
                        cache_hit=None,
                        retrieval_status=None,
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
