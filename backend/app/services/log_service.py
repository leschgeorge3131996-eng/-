from __future__ import annotations

import json
import logging
from collections import Counter
from statistics import mean

from ..core.config import Settings, get_settings
from ..schemas.log import CallLogEntry

logger = logging.getLogger(__name__)


class LogService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.log_file = self.settings.logs_dir / "call_logs.jsonl"

    def write_log(self, entry: CallLogEntry) -> None:
        with self.log_file.open("a", encoding="utf-8") as file:
            file.write(json.dumps(entry.model_dump(), ensure_ascii=False) + "\n")

    def list_logs(self, limit: int = 20) -> list[dict]:
        entries = self._load_entries(limit=limit)
        return list(reversed(entries))

    def summarize_logs(self, limit: int | None = None) -> dict:
        entries = self._load_entries(limit=limit)
        if not entries:
            return {
                "total_requests": 0,
                "success_count": 0,
                "failure_count": 0,
                "success_rate": 0.0,
                "average_latency_ms": 0,
                "p95_latency_ms": 0,
                "cache_hit_count": 0,
                "retrieval_applied_count": 0,
                "citation_count_sum": 0,
                "answered_count": 0,
                "refused_count": 0,
                "error_count": 0,
                "answered_rate": 0.0,
                "refused_rate": 0.0,
                "token_total_sum": 0,
                "by_task": {},
                "by_model": {},
                "by_outcome": {},
                "by_retrieval_status": {},
                "error_types": {},
            }

        latencies = sorted(
            int(entry.get("latency_ms", 0))
            for entry in entries
            if isinstance(entry.get("latency_ms"), int | float)
        )
        success_count = sum(1 for entry in entries if entry.get("success") is True)
        failure_count = len(entries) - success_count
        cache_hit_count = sum(1 for entry in entries if entry.get("cache_hit") is True)
        retrieval_applied_count = sum(
            1 for entry in entries if entry.get("retrieval_applied") is True
        )
        citation_count_sum = sum(
            int((entry.get("extra") or {}).get("citation_count", 0) or 0)
            for entry in entries
            if isinstance(entry.get("extra"), dict)
        )
        token_total_sum = sum(
            int(entry.get("token_total", 0) or 0)
            for entry in entries
        )
        by_task_counter = Counter(str(entry.get("task_type", "unknown")) for entry in entries)
        by_model_counter = Counter(str(entry.get("model_name", "unknown")) for entry in entries)
        outcome_counter = Counter(
            str(entry.get("outcome", "unknown"))
            for entry in entries
        )
        retrieval_status_counter = Counter(
            str(entry.get("retrieval_status"))
            for entry in entries
            if entry.get("retrieval_status")
        )
        error_types_counter = Counter(
            str(entry.get("error_type"))
            for entry in entries
            if entry.get("error_type")
        )

        return {
            "total_requests": len(entries),
            "success_count": success_count,
            "failure_count": failure_count,
            "success_rate": round(success_count / len(entries), 4),
            "average_latency_ms": int(mean(latencies)) if latencies else 0,
            "p95_latency_ms": self._percentile(latencies, 0.95),
            "cache_hit_count": cache_hit_count,
            "retrieval_applied_count": retrieval_applied_count,
            "citation_count_sum": citation_count_sum,
            "answered_count": outcome_counter.get("answered", 0),
            "refused_count": outcome_counter.get("refused", 0),
            "error_count": outcome_counter.get("error", 0),
            "answered_rate": round(outcome_counter.get("answered", 0) / len(entries), 4),
            "refused_rate": round(outcome_counter.get("refused", 0) / len(entries), 4),
            "token_total_sum": token_total_sum,
            "time_range": {
                "first_timestamp": entries[0].get("timestamp"),
                "last_timestamp": entries[-1].get("timestamp"),
            },
            "by_task": dict(by_task_counter),
            "by_model": dict(by_model_counter),
            "by_outcome": dict(outcome_counter),
            "by_retrieval_status": dict(retrieval_status_counter),
            "error_types": dict(error_types_counter),
        }

    def _load_entries(self, limit: int | None = None) -> list[dict]:
        if not self.log_file.exists():
            return []

        lines = self.log_file.read_text(encoding="utf-8").splitlines()
        if limit is not None:
            lines = lines[-limit:]
        results: list[dict] = []
        for line in lines:
            if not line.strip():
                continue
            try:
                results.append(json.loads(line))
            except json.JSONDecodeError:
                logger.warning("Skip malformed JSONL log line")
        return results

    def _percentile(self, values: list[int], ratio: float) -> int:
        if not values:
            return 0
        index = max(0, min(len(values) - 1, int((len(values) - 1) * ratio)))
        return values[index]
