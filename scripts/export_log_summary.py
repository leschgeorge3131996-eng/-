from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.services.log_service import LogService


def render_markdown(summary: dict) -> str:
    lines = [
        "# Log Summary",
        "",
        f"- Total requests: {summary['total_requests']}",
        f"- Success count: {summary['success_count']}",
        f"- Failure count: {summary['failure_count']}",
        f"- Success rate: {summary['success_rate']}",
        f"- Average latency (ms): {summary['average_latency_ms']}",
        f"- P95 latency (ms): {summary['p95_latency_ms']}",
        f"- Cache hit count: {summary['cache_hit_count']}",
        f"- Token total sum: {summary['token_total_sum']}",
        "",
        "## By Task",
    ]
    for task, count in summary["by_task"].items():
        lines.append(f"- {task}: {count}")

    lines.extend(["", "## By Model"])
    for model, count in summary["by_model"].items():
        lines.append(f"- {model}: {count}")

    lines.extend(["", "## Error Types"])
    if summary["error_types"]:
        for error_type, count in summary["error_types"].items():
            lines.append(f"- {error_type}: {count}")
    else:
        lines.append("- none")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Export call log summary.")
    parser.add_argument("--limit", type=int, default=None, help="Summarize only the latest N entries.")
    parser.add_argument(
        "--format",
        choices=["json", "md"],
        default="json",
        help="Output format.",
    )
    parser.add_argument("--output", type=str, default=None, help="Optional output file path.")
    args = parser.parse_args()

    service = LogService()
    summary = service.summarize_logs(limit=args.limit)

    rendered = (
        json.dumps(summary, ensure_ascii=False, indent=2)
        if args.format == "json"
        else render_markdown(summary)
    )

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
        print(f"Saved summary to {output_path}")
        return

    print(rendered)


if __name__ == "__main__":
    main()

