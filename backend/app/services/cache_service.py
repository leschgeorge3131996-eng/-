from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from ..core.config import Settings, get_settings


class CacheService:
    cache_version = "v5"

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def build_cache_key(
        self,
        *,
        document_fingerprint: str,
        task_type: str,
        user_input: str | None,
        model_name: str,
    ) -> str:
        normalized_input = (user_input or "").strip()
        raw_key = "::".join(
            [
                self.cache_version,
                document_fingerprint,
                task_type,
                model_name,
                normalized_input,
            ]
        )
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    def get(self, cache_key: str) -> dict[str, Any] | None:
        cache_path = self._cache_path(cache_key)
        if not cache_path.exists():
            return None

        try:
            return json.loads(cache_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None

    def set(self, cache_key: str, payload: dict[str, Any]) -> None:
        cache_path = self._cache_path(cache_key)
        cache_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _cache_path(self, cache_key: str) -> Path:
        return self.settings.cache_dir / f"{cache_key}.json"
