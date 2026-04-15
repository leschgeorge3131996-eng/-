from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class CallLogEntry(BaseModel):
    request_id: str
    timestamp: str
    endpoint: str
    task_type: str
    model_name: str
    route_tier: str | None = None
    route_model: str | None = None
    route_reason: str | None = None
    file_id: str | None = None
    success: bool
    outcome: str = "answered"
    latency_ms: int
    prompt_chars: int
    output_chars: int
    token_in: int | None = None
    token_out: int | None = None
    token_total: int | None = None
    cache_hit: bool = False
    retrieval_status: str | None = None
    retrieval_applied: bool = False
    retrieved_chunk_count: int = 0
    context_truncated: bool = False
    error_message: str | None = None
    error_type: str | None = None
    extra: dict[str, Any] | None = None
