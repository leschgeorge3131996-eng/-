from __future__ import annotations

import logging
from datetime import datetime, timezone
from time import perf_counter
from uuid import uuid4

from ..core.exceptions import AppError
from ..schemas.log import CallLogEntry
from ..schemas.task import TaskResult, TaskType
from .cache_service import CacheService
from .file_service import FileService
from .log_service import LogService
from .model_client import ModelClient

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(
        self,
        file_service: FileService | None = None,
        model_client: ModelClient | None = None,
        log_service: LogService | None = None,
        cache_service: CacheService | None = None,
    ) -> None:
        self.file_service = file_service or FileService()
        self.model_client = model_client or ModelClient()
        self.log_service = log_service or LogService()
        self.cache_service = cache_service or CacheService(settings=self.file_service.settings)

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

        try:
            metadata = self.file_service.get_document_metadata(file_id)
            document_text = self.file_service.get_document_text(file_id)
            resolved_model_name = self.model_client.resolve_model_name(task_type)
            cache_key = self.cache_service.build_cache_key(
                document_text=document_text,
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
                    model_name=cached_result["model_name"],
                    latency_ms=latency_ms,
                    result=cached_result["result"],
                    cache_hit=True,
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
                        context_truncated=task_result.context_truncated,
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
                    context_truncated=model_result.context_truncated,
                )
            )

            return TaskResult(
                request_id=request_id,
                task_type=task_type,
                file_id=file_id,
                document_name=metadata.original_name,
                model_name=model_result.model_name,
                latency_ms=latency_ms,
                result=model_result.content,
                cache_hit=False,
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
                    context_truncated=False,
                    error_message=exc.message,
                    error_type=exc.code,
                    extra=exc.details,
                )
            )
            logger.exception("Task failed: %s", exc.message)
            raise

    def _safe_write_log(self, entry: CallLogEntry) -> None:
        try:
            self.log_service.write_log(entry)
        except Exception:
            logger.exception("Failed to write call log")
