from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


TaskType = Literal["ask", "summary", "outline"]


class AskRequest(BaseModel):
    file_id: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1, max_length=4000)


class TaskRequest(BaseModel):
    file_id: str = Field(..., min_length=1)
    instruction: str | None = Field(default=None, max_length=4000)


class TokenUsage(BaseModel):
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


class ModelResult(BaseModel):
    content: str
    model_name: str
    prompt_chars: int
    output_chars: int
    source_document_chars: int
    used_document_chars: int
    truncation_message: str | None = None
    token_usage: TokenUsage | None = None
    context_truncated: bool = False


class TaskResult(BaseModel):
    request_id: str
    task_type: TaskType
    file_id: str
    document_name: str
    document_fingerprint: str | None = None
    model_name: str
    latency_ms: int
    result: str
    cache_hit: bool = False
    source_document_chars: int = 0
    used_document_chars: int = 0
    truncation_message: str | None = None
    context_truncated: bool = False
    token_usage: TokenUsage | None = None
