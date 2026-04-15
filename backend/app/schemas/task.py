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
    token_usage: TokenUsage | None = None
    context_truncated: bool = False


class TaskResult(BaseModel):
    request_id: str
    task_type: TaskType
    file_id: str
    document_name: str
    model_name: str
    latency_ms: int
    result: str
    cache_hit: bool = False
    context_truncated: bool = False
    token_usage: TokenUsage | None = None
