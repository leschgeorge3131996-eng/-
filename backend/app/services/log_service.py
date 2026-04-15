from __future__ import annotations

import json
import logging

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
        if not self.log_file.exists():
            return []

        lines = self.log_file.read_text(encoding="utf-8").splitlines()
        results: list[dict] = []
        for line in reversed(lines[-limit:]):
            if not line.strip():
                continue
            try:
                results.append(json.loads(line))
            except json.JSONDecodeError:
                logger.warning("Skip malformed JSONL log line")
        return results
