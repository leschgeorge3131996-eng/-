from __future__ import annotations

import logging
from datetime import datetime, timezone
from time import perf_counter
from uuid import uuid4

from ..core.exceptions import AppError
from ..schemas.log import CallLogEntry
from ..schemas.task import Citation, TaskResult, TaskType
from .cache_service import CacheService
from .context_planner import ContextPlannerService
from .file_service import FileService
from .log_service import LogService
from .model_client import ModelClient
from .retrieval_service import RetrievalService

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(
        self,
        file_service: FileService | None = None,
        model_client: ModelClient | None = None,
        log_service: LogService | None = None,
        cache_service: CacheService | None = None,
        retrieval_service: RetrievalService | None = None,
        context_planner: ContextPlannerService | None = None,
    ) -> None:
        self.file_service = file_service or FileService()
        self.model_client = model_client or ModelClient()
        self.log_service = log_service or LogService()
        self.cache_service = cache_service or CacheService(settings=self.file_service.settings)
        self.retrieval_service = retrieval_service or RetrievalService()
        self.context_planner = context_planner or ContextPlannerService(self.retrieval_service)

    def run_task(
        self,
        *,
        task_type: TaskType,
        endpoint: str,
        file_id: str,
        user_input: str | None = None,
    ) -> TaskResult:
        request_id = uuid4().hex
        started_at = datetime.now(timezone.utc).isoformat()
        started_timer = perf_counter()
        metadata = None
        document_text = ""
        retrieval_status = "not_used"
        retrieval_applied = False
        retrieved_chunk_count = 0
        retrieved_pages: list[int] = []
        citations: list[Citation] = []
        context_strategy = "full_text"

        try:
            metadata = self.file_service.get_document_metadata(file_id)
            raw_document_text = self.file_service.get_document_text(file_id)
            chunked_document = self.file_service.get_document_chunks(file_id)
            planned_context = self.context_planner.plan(
                task_type=task_type,
                user_input=user_input,
                raw_text=raw_document_text,
                chunked_document=chunked_document,
            )
            document_text = planned_context.document_text
            context_strategy = planned_context.strategy
            selected_chunks = planned_context.selected_chunks
            if task_type == "ask":
                retrieval_status = "matched" if selected_chunks else "no_match"
            elif selected_chunks:
                retrieval_status = "coverage"
            if selected_chunks:
                retrieved_chunk_count = len(selected_chunks)
                retrieved_pages = sorted(
                    {page for chunk in selected_chunks for page in chunk.page_numbers}
                )
                citations = [
                    Citation(
                        chunk_id=chunk.chunk_id,
                        page_numbers=chunk.page_numbers,
                        snippet=(
                            chunk.text[:220].strip() + "..."
                            if len(chunk.text) > 220
                            else chunk.text
                        ),
                        )
                        for chunk in selected_chunks
                    ]
            if task_type == "ask" and selected_chunks:
                retrieval_applied = True

            if task_type == "ask" and not selected_chunks:
                latency_ms = int((perf_counter() - started_timer) * 1000)
                refusal_text = "未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。"
                task_result = TaskResult(
                    request_id=request_id,
                    task_type=task_type,
                    file_id=file_id,
                    document_name=metadata.original_name,
                    document_fingerprint=metadata.document_fingerprint,
                    model_name=self.model_client.resolve_model_name(task_type),
                    latency_ms=latency_ms,
                    result=refusal_text,
                    cache_hit=False,
                    retrieval_status=retrieval_status,
                    retrieval_message="当前问题与检索到的文档片段相关性不足，系统已拒绝无依据回答。",
                    retrieval_applied=False,
                    retrieved_chunk_count=0,
                    retrieved_pages=[],
                    citations=[],
                    source_document_chars=len(raw_document_text),
                    used_document_chars=0,
                    truncation_message=None,
                    context_truncated=False,
                    token_usage=None,
                )
                self._safe_write_log(
                    CallLogEntry(
                        request_id=request_id,
                        timestamp=started_at,
                        endpoint=endpoint,
                        task_type=task_type,
                        model_name=task_result.model_name,
                        file_id=file_id,
                        success=True,
                        latency_ms=latency_ms,
                        prompt_chars=len(user_input or ""),
                        output_chars=len(refusal_text),
                        cache_hit=False,
                        retrieval_status=retrieval_status,
                        retrieval_applied=False,
                        retrieved_chunk_count=0,
                        context_truncated=False,
                        extra={
                            "context_strategy": context_strategy,
                            "retrieved_pages": [],
                            "citation_count": 0,
                            "degraded_without_answer": True,
                        },
                    )
                )
                return task_result

            resolved_model_name = self.model_client.resolve_model_name(task_type)
            cache_key = self.cache_service.build_cache_key(
                document_fingerprint=metadata.document_fingerprint or "",
                task_type=task_type,
                user_input=user_input,
                model_name=resolved_model_name,
            )
            cached_result = self.cache_service.get(cache_key)
            if cached_result is not None:
                latency_ms = int((perf_counter() - started_timer) * 1000)
                task_result = TaskResult(
                    request_id=request_id,
                    task_type=task_type,
                    file_id=file_id,
                    document_name=metadata.original_name,
                    document_fingerprint=metadata.document_fingerprint,
                    model_name=cached_result["model_name"],
                    latency_ms=latency_ms,
                    result=cached_result["result"],
                    cache_hit=True,
                    retrieval_status=cached_result.get("retrieval_status", retrieval_status),
                    retrieval_message=cached_result.get("retrieval_message"),
                    retrieval_applied=cached_result.get("retrieval_applied", retrieval_applied),
                    retrieved_chunk_count=cached_result.get(
                        "retrieved_chunk_count",
                        retrieved_chunk_count,
                    ),
                    retrieved_pages=cached_result.get("retrieved_pages", retrieved_pages),
                    citations=[
                        Citation.model_validate(item)
                        for item in cached_result.get("citations", [])
                    ],
                    source_document_chars=cached_result.get("source_document_chars", 0),
                    used_document_chars=cached_result.get("used_document_chars", 0),
                    truncation_message=cached_result.get("truncation_message"),
                    context_truncated=cached_result.get("context_truncated", False),
                    token_usage=cached_result.get("token_usage"),
                )
                self._safe_write_log(
                    CallLogEntry(
                        request_id=request_id,
                        timestamp=started_at,
                        endpoint=endpoint,
                        task_type=task_type,
                        model_name=task_result.model_name,
                        file_id=file_id,
                        success=True,
                        latency_ms=latency_ms,
                        prompt_chars=cached_result.get("prompt_chars", 0),
                        output_chars=len(task_result.result),
                        token_in=(
                            task_result.token_usage.prompt_tokens
                            if task_result.token_usage
                            else None
                        ),
                        token_out=(
                            task_result.token_usage.completion_tokens
                            if task_result.token_usage
                            else None
                        ),
                        token_total=(
                            task_result.token_usage.total_tokens
                            if task_result.token_usage
                            else None
                        ),
                        cache_hit=True,
                        retrieval_status=task_result.retrieval_status,
                        retrieval_applied=task_result.retrieval_applied,
                        retrieved_chunk_count=task_result.retrieved_chunk_count,
                        context_truncated=task_result.context_truncated,
                        extra={
                            "context_strategy": cached_result.get("context_strategy", context_strategy),
                            "retrieved_pages": task_result.retrieved_pages,
                            "citation_count": len(task_result.citations),
                        },
                    )
                )
                return task_result

            model_result = self.model_client.call_model(
                task_type=task_type,
                document_text=document_text,
                user_input=user_input,
            )
            latency_ms = int((perf_counter() - started_timer) * 1000)
            self.cache_service.set(
                cache_key,
                {
                    "task_type": task_type,
                    "model_name": model_result.model_name,
                    "result": model_result.content,
                    "context_strategy": context_strategy,
                    "retrieval_status": retrieval_status,
                    "retrieval_message": None,
                    "retrieval_applied": retrieval_applied,
                    "retrieved_chunk_count": retrieved_chunk_count,
                    "retrieved_pages": retrieved_pages,
                    "citations": [citation.model_dump() for citation in citations],
                    "source_document_chars": model_result.source_document_chars,
                    "used_document_chars": model_result.used_document_chars,
                    "truncation_message": model_result.truncation_message,
                    "context_truncated": model_result.context_truncated,
                    "prompt_chars": model_result.prompt_chars,
                    "token_usage": (
                        model_result.token_usage.model_dump()
                        if model_result.token_usage
                        else None
                    ),
                },
            )
            self._safe_write_log(
                CallLogEntry(
                    request_id=request_id,
                    timestamp=started_at,
                    endpoint=endpoint,
                    task_type=task_type,
                    model_name=model_result.model_name,
                    file_id=file_id,
                    success=True,
                    latency_ms=latency_ms,
                    prompt_chars=model_result.prompt_chars,
                    output_chars=model_result.output_chars,
                    token_in=(
                        model_result.token_usage.prompt_tokens
                        if model_result.token_usage
                        else None
                    ),
                    token_out=(
                        model_result.token_usage.completion_tokens
                        if model_result.token_usage
                        else None
                    ),
                    token_total=(
                        model_result.token_usage.total_tokens
                        if model_result.token_usage
                        else None
                    ),
                    cache_hit=False,
                    retrieval_status=retrieval_status,
                    retrieval_applied=retrieval_applied,
                    retrieved_chunk_count=retrieved_chunk_count,
                    context_truncated=model_result.context_truncated,
                    extra=(
                        {
                            "context_strategy": context_strategy,
                            "retrieved_pages": retrieved_pages,
                            "citation_count": len(citations),
                        }
                        if retrieved_pages or citations
                        else None
                    ),
                )
            )

            return TaskResult(
                request_id=request_id,
                task_type=task_type,
                file_id=file_id,
                document_name=metadata.original_name,
                document_fingerprint=metadata.document_fingerprint,
                model_name=model_result.model_name,
                latency_ms=latency_ms,
                result=model_result.content,
                cache_hit=False,
                retrieval_status=retrieval_status,
                retrieval_message=None,
                retrieval_applied=retrieval_applied,
                retrieved_chunk_count=retrieved_chunk_count,
                retrieved_pages=retrieved_pages,
                citations=citations,
                source_document_chars=model_result.source_document_chars,
                used_document_chars=model_result.used_document_chars,
                truncation_message=model_result.truncation_message,
                context_truncated=model_result.context_truncated,
                token_usage=model_result.token_usage,
            )
        except AppError as exc:
            latency_ms = int((perf_counter() - started_timer) * 1000)
            self._safe_write_log(
                CallLogEntry(
                    request_id=request_id,
                    timestamp=started_at,
                    endpoint=endpoint,
                    task_type=task_type,
                    model_name=self.model_client.resolve_model_name(task_type),
                    file_id=file_id if metadata or file_id else None,
                    success=False,
                    latency_ms=latency_ms,
                    prompt_chars=len(document_text) + len(user_input or ""),
                    output_chars=0,
                    cache_hit=False,
                    retrieval_status=retrieval_status,
                    retrieval_applied=retrieval_applied,
                    retrieved_chunk_count=retrieved_chunk_count,
                    context_truncated=False,
                    error_message=exc.message,
                    error_type=exc.code,
                    extra=(
                        {
                            "context_strategy": context_strategy,
                            "retrieved_pages": retrieved_pages,
                            "citation_count": len(citations),
                            **exc.details,
                        }
                        if retrieved_pages
                        else exc.details
                    ),
                )
            )
            logger.exception("Task failed: %s", exc.message)
            raise

    def _safe_write_log(self, entry: CallLogEntry) -> None:
        try:
            self.log_service.write_log(entry)
        except Exception:
            logger.exception("Failed to write call log")
