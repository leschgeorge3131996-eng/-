from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from .document import BBoxRegion


TaskType = Literal["ask", "summary", "outline"]
ResponseDetailLevel = Literal["concise", "balanced", "detailed"]
EvidenceMode = Literal["declared", "candidate", "none"]


class AskRequest(BaseModel):
    file_id: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1, max_length=4000)
    document_access_token: str | None = Field(default=None, min_length=1)
    response_detail_level: ResponseDetailLevel = "balanced"


class TaskRequest(BaseModel):
    file_id: str = Field(..., min_length=1)
    instruction: str | None = Field(default=None, max_length=4000)
    document_access_token: str | None = Field(default=None, min_length=1)
    response_detail_level: ResponseDetailLevel = "balanced"


class TokenUsage(BaseModel):
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


class Citation(BaseModel):
    chunk_id: str
    page_numbers: list[int]
    snippet: str
    bbox_regions: list[BBoxRegion] = []


class EvidenceQuote(BaseModel):
    chunk_id: str
    quote: str


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
    route_tier: str = "task_specific"
    route_model: str | None = None
    route_reason: str | None = None
    response_detail_level: ResponseDetailLevel = "balanced"
    latency_ms: int
    result: str
    outcome: str = "answered"
    cache_hit: bool = False
    retrieval_status: str = "not_used"
    retrieval_message: str | None = None
    retrieval_applied: bool = False
    evidence_mode: EvidenceMode = "none"
    retrieved_chunk_count: int = 0
    retrieved_pages: list[int] = []
    used_chunk_ids: list[str] = []
    evidence_quotes: list[EvidenceQuote] = []
    citations: list[Citation] = []
    candidate_chunks: list[Citation] = []
    source_chunks: list[Citation] = []
    source_document_chars: int = 0
    used_document_chars: int = 0
    truncation_message: str | None = None
    context_truncated: bool = False
    token_usage: TokenUsage | None = None
