from __future__ import annotations

import json
import logging
import re
from datetime import datetime, timezone
from time import perf_counter
from uuid import uuid4

from ..core.exceptions import AppError
from ..schemas.document import ParsedChunk, ParsedLine
from ..schemas.log import CallLogEntry
from ..schemas.task import (
    Citation,
    EvidenceQuote,
    ModelResult,
    ResponseDetailLevel,
    TaskResult,
    TaskType,
)
from .bbox_matcher import match_snippet_to_line_bboxes
from .cache_service import CacheService
from .context_planner import ContextPlannerService
from .file_service import FileService
from .log_service import LogService
from .model_client import ModelClient
from .retrieval_service import RetrievalService

logger = logging.getLogger(__name__)


class TaskService:
    ASK_EVIDENCE_MAX_ATTEMPTS = 2
    AGENTIC_ASK_MAX_ITERS = 2
    AGENTIC_ASK_MAX_CHUNKS = 8

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
        session_id: str | None = None,
        document_access_token: str | None = None,
        user_input: str | None = None,
        response_detail_level: ResponseDetailLevel = "balanced",
    ) -> TaskResult:
        request_id = uuid4().hex
        started_at = datetime.now(timezone.utc).isoformat()
        started_timer = perf_counter()
        metadata = None
        document_text = ""
        retrieval_status = "not_used"
        retrieval_applied = False
        evidence_mode = "none"
        retrieved_chunk_count = 0
        retrieved_pages: list[int] = []
        citations: list[Citation] = []
        candidate_chunks: list[Citation] = []
        source_chunks: list[Citation] = []
        context_strategy = "full_text"
        outcome = "answered"
        route_tier = "task_specific"
        route_model: str | None = None
        route_reason: str | None = None
        ask_evidence_retry_count = 0
        agent_iterations = 1
        query_rewrites: list[str] = []
        platform_request_id: str | None = None
        low_confidence_review = False
        low_confidence_review_failed = False

        try:
            metadata = self.file_service.get_document_metadata(
                file_id,
                access_token=document_access_token,
                session_id=session_id,
            )
            pages_index = self._build_pages_index(
                file_id,
                access_token=document_access_token,
                session_id=session_id,
            )
            raw_document_text = self.file_service.get_document_text(
                file_id,
                access_token=document_access_token,
                session_id=session_id,
            )
            chunked_document = self.file_service.get_document_chunks(
                file_id,
                access_token=document_access_token,
                session_id=session_id,
            )
            planned_context = self.context_planner.plan(
                task_type=task_type,
                user_input=user_input,
                raw_text=raw_document_text,
                chunked_document=chunked_document,
                file_id=file_id,
            )
            document_text = planned_context.document_text
            context_strategy = planned_context.strategy
            selected_chunks = planned_context.selected_chunks
            if task_type == "ask":
                if not selected_chunks:
                    retrieval_status = "no_match"
                elif not planned_context.retrieval_confident:
                    retrieval_status = "low_confidence"
                    low_confidence_review = True
                else:
                    retrieval_status = "matched"
            elif selected_chunks:
                retrieval_status = "coverage"
            if selected_chunks:
                retrieved_chunk_count = len(selected_chunks)
                retrieved_pages = sorted(
                    {page for chunk in selected_chunks for page in chunk.page_numbers}
                )
                if task_type == "ask":
                    evidence_mode = "candidate"
                    citations = []
                    candidate_chunks = [
                        self._build_chunk_ref(chunk)
                        for chunk in self._select_display_chunks(selected_chunks, limit=3)
                    ]
                    self._attach_line_bboxes(candidate_chunks, pages_index)
                else:
                    display_chunks = self._select_display_chunks(selected_chunks, limit=3)
                    source_chunks = [self._build_chunk_ref(chunk) for chunk in display_chunks]
                    self._attach_line_bboxes(source_chunks, pages_index)
            if task_type == "ask" and selected_chunks:
                retrieval_applied = True

            if task_type == "ask" and not selected_chunks:
                latency_ms = int((perf_counter() - started_timer) * 1000)
                refusal_text = "未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。"
                route_tier = "none"
                route_model = None
                route_reason = "retrieval_no_match"
                task_result = TaskResult(
                    request_id=request_id,
                    task_type=task_type,
                    file_id=file_id,
                    document_name=metadata.original_name,
                    document_fingerprint=metadata.document_fingerprint,
                    model_name="retrieval_gate",
                    route_tier=route_tier,
                    route_model=route_model,
                    route_reason=route_reason,
                    response_detail_level=response_detail_level,
                    latency_ms=latency_ms,
                    result=refusal_text,
                    outcome="refused",
                    cache_hit=False,
                    retrieval_status=retrieval_status,
                    retrieval_message="当前问题与检索到的文档片段相关性不足，系统已拒绝无依据回答。",
                    retrieval_applied=False,
                    evidence_mode="none",
                    retrieved_chunk_count=0,
                    retrieved_pages=[],
                    citations=[],
                    candidate_chunks=[],
                    source_chunks=[],
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
                        route_tier=route_tier,
                        route_model=route_model,
                        route_reason=route_reason,
                        response_detail_level=response_detail_level,
                        file_id=file_id,
                        success=True,
                        outcome="refused",
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
                            "evidence_mode": "none",
                            "citation_count": 0,
                            "source_chunk_count": 0,
                            "degraded_without_answer": True,
                        },
                    )
                )
                return task_result

            route_decision = self.model_client.resolve_route(
                task_type=task_type,
                user_input=user_input,
                source_document_chars=len(document_text) if document_text else len(raw_document_text),
            )
            resolved_model_name = route_decision.model_name
            route_tier = route_decision.route_tier
            route_model = route_decision.model_name
            route_reason = route_decision.route_reason
            cache_key = self.cache_service.build_cache_key(
                document_fingerprint=metadata.document_fingerprint or "",
                task_type=task_type,
                user_input=user_input,
                model_name=resolved_model_name,
                response_detail_level=response_detail_level,
            )
            cached_result = self.cache_service.get(cache_key)
            if cached_result is not None:
                latency_ms = int((perf_counter() - started_timer) * 1000)
                cached_evidence_quotes = [
                    EvidenceQuote.model_validate(item)
                    for item in cached_result.get("evidence_quotes", [])
                ]
                cached_citations = [
                    Citation.model_validate(item)
                    for item in cached_result.get("citations", [])
                ]
                cached_candidate_chunks = [
                    Citation.model_validate(item)
                    for item in cached_result.get("candidate_chunks", [])
                ]
                cached_source_chunks = [
                    Citation.model_validate(item)
                    for item in cached_result.get("source_chunks", [])
                ]
                cached_quote_by_chunk = {
                    quote.chunk_id: quote.quote for quote in cached_evidence_quotes
                }
                self._attach_line_bboxes(
                    cached_citations, pages_index, quote_by_chunk=cached_quote_by_chunk
                )
                self._attach_line_bboxes(cached_candidate_chunks, pages_index)
                self._attach_line_bboxes(cached_source_chunks, pages_index)
                task_result = TaskResult(
                    request_id=request_id,
                    task_type=task_type,
                    file_id=file_id,
                    document_name=metadata.original_name,
                    document_fingerprint=metadata.document_fingerprint,
                    model_name=cached_result["model_name"],
                    route_tier=cached_result.get("route_tier", route_tier),
                    route_model=cached_result.get("route_model", route_model),
                    route_reason=cached_result.get("route_reason", route_reason),
                    response_detail_level=cached_result.get("response_detail_level", response_detail_level),
                    latency_ms=latency_ms,
                    result=cached_result["result"],
                    outcome=cached_result.get("outcome", outcome),
                    cache_hit=True,
                    retrieval_status=cached_result.get("retrieval_status", retrieval_status),
                    retrieval_message=cached_result.get("retrieval_message"),
                    retrieval_applied=cached_result.get("retrieval_applied", retrieval_applied),
                    evidence_mode=cached_result.get("evidence_mode", evidence_mode),
                    retrieved_chunk_count=cached_result.get(
                        "retrieved_chunk_count",
                        retrieved_chunk_count,
                    ),
                    retrieved_pages=cached_result.get("retrieved_pages", retrieved_pages),
                    used_chunk_ids=cached_result.get("used_chunk_ids", []),
                    evidence_quotes=cached_evidence_quotes,
                    citations=cached_citations,
                    candidate_chunks=cached_candidate_chunks,
                    source_chunks=cached_source_chunks,
                    source_document_chars=cached_result.get("source_document_chars", 0),
                    used_document_chars=cached_result.get("used_document_chars", 0),
                    truncation_message=cached_result.get("truncation_message"),
                    context_truncated=cached_result.get("context_truncated", False),
                    token_usage=cached_result.get("token_usage"),
                    platform_request_id=cached_result.get("platform_request_id"),
                    agent_iterations=cached_result.get("agent_iterations", 1),
                    query_rewrites=cached_result.get("query_rewrites", []),
                )
                self._safe_write_log(
                    CallLogEntry(
                        request_id=request_id,
                        platform_request_id=cached_result.get("platform_request_id"),
                        timestamp=started_at,
                        endpoint=endpoint,
                        task_type=task_type,
                        model_name=task_result.model_name,
                        route_tier=task_result.route_tier,
                        route_model=task_result.route_model,
                        route_reason=task_result.route_reason,
                        response_detail_level=task_result.response_detail_level,
                        file_id=file_id,
                        success=True,
                        outcome=task_result.outcome,
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
                            "evidence_mode": task_result.evidence_mode,
                            "used_chunk_count": len(task_result.used_chunk_ids),
                            "citation_count": len(task_result.citations),
                            "candidate_chunk_count": len(task_result.candidate_chunks),
                            "source_chunk_count": len(task_result.source_chunks),
                            "ask_evidence_retry_count": cached_result.get(
                                "ask_evidence_retry_count",
                                0,
                            ),
                            "agent_iterations": cached_result.get("agent_iterations", 1),
                            "query_rewrites": cached_result.get("query_rewrites", []),
                        },
                    )
                )
                return task_result

            result_content = ""
            used_chunk_ids: list[str] = []
            evidence_quotes: list[EvidenceQuote] = []
            llm_refused = False
            if task_type == "ask" and selected_chunks:
                (
                    model_result,
                    result_content,
                    used_chunk_ids,
                    evidence_quotes,
                    ask_evidence_retry_count,
                    llm_refused,
                    selected_chunks,
                    agent_iterations,
                    query_rewrites,
                ) = self._run_agentic_ask(
                    chunked_document=chunked_document,
                    selected_chunks=selected_chunks,
                    user_input=user_input,
                    model_name_override=resolved_model_name,
                    response_detail_level=response_detail_level,
                    file_id=file_id,
                )
                # agentic re-retrieval may expand the evidence set; refresh telemetry + display chunks
                retrieved_chunk_count = len(selected_chunks)
                retrieved_pages = sorted(
                    {page for chunk in selected_chunks for page in chunk.page_numbers}
                )
                candidate_chunks = [
                    self._build_chunk_ref(chunk)
                    for chunk in self._select_display_chunks(selected_chunks, limit=3)
                ]
                self._attach_line_bboxes(candidate_chunks, pages_index)
                if low_confidence_review and not llm_refused and not (used_chunk_ids and evidence_quotes):
                    llm_refused = True
                    low_confidence_review_failed = True
                    result_content = (
                        "检索到候选片段，但模型未能返回可验证的逐字原文证据，"
                        "系统已拒绝回答以避免无依据结论。"
                    )
                    used_chunk_ids = []
                    evidence_quotes = []
            else:
                model_result = self.model_client.call_model(
                    task_type=task_type,
                    document_text=document_text,
                    user_input=user_input,
                    model_name_override=resolved_model_name,
                    response_detail_level=response_detail_level,
                )
                result_content = model_result.content

            platform_request_id = model_result.platform_request_id

            if task_type == "ask" and llm_refused:
                latency_ms = int((perf_counter() - started_timer) * 1000)
                refusal_text = (
                    result_content
                    or "未在文档中检索到能直接回答该问题的依据。请换一个更贴近文档内容的问题。"
                )
                refusal_retrieval_message = (
                    "低置信候选片段已交由模型复核，但模型未返回可验证的逐字证据，已拒答。"
                    if low_confidence_review_failed
                    else "检索命中但模型判定文档中无直接依据，已拒答。"
                )
                task_result = TaskResult(
                    request_id=request_id,
                    task_type=task_type,
                    file_id=file_id,
                    document_name=metadata.original_name,
                    document_fingerprint=metadata.document_fingerprint,
                    model_name=model_result.model_name,
                    route_tier=route_tier,
                    route_model=route_model,
                    route_reason="llm_refused",
                    response_detail_level=response_detail_level,
                    latency_ms=latency_ms,
                    result=refusal_text,
                    outcome="refused",
                    cache_hit=False,
                    retrieval_status=retrieval_status,
                    retrieval_message=refusal_retrieval_message,
                    retrieval_applied=retrieval_applied,
                    evidence_mode="none",
                    retrieved_chunk_count=retrieved_chunk_count,
                    retrieved_pages=retrieved_pages,
                    used_chunk_ids=[],
                    evidence_quotes=[],
                    citations=[],
                    candidate_chunks=candidate_chunks,
                    source_chunks=source_chunks,
                    source_document_chars=model_result.source_document_chars,
                    used_document_chars=model_result.used_document_chars,
                    truncation_message=model_result.truncation_message,
                    context_truncated=model_result.context_truncated,
                    token_usage=model_result.token_usage,
                    platform_request_id=platform_request_id,
                    agent_iterations=agent_iterations,
                    query_rewrites=query_rewrites,
                )
                self._safe_write_log(
                    CallLogEntry(
                        request_id=request_id,
                        platform_request_id=platform_request_id,
                        timestamp=started_at,
                        endpoint=endpoint,
                        task_type=task_type,
                        model_name=model_result.model_name,
                        route_tier=route_tier,
                        route_model=route_model,
                        route_reason="llm_refused",
                        response_detail_level=response_detail_level,
                        file_id=file_id,
                        success=True,
                        outcome="refused",
                        latency_ms=latency_ms,
                        prompt_chars=model_result.prompt_chars,
                        output_chars=len(refusal_text),
                        cache_hit=False,
                        retrieval_status=retrieval_status,
                        retrieval_applied=retrieval_applied,
                        retrieved_chunk_count=retrieved_chunk_count,
                        context_truncated=model_result.context_truncated,
                        extra={
                            "context_strategy": context_strategy,
                            "retrieved_pages": retrieved_pages,
                            "evidence_mode": "none",
                            "citation_count": 0,
                            "ask_evidence_retry_count": ask_evidence_retry_count,
                            "agent_iterations": agent_iterations,
                            "query_rewrites": query_rewrites,
                            "llm_refused": True,
                            "low_confidence_review": low_confidence_review,
                            "low_confidence_review_failed": low_confidence_review_failed,
                        },
                    )
                )
                return task_result
            if task_type == "ask" and selected_chunks:
                if used_chunk_ids:
                    evidence_mode = "declared"
                    selected_by_id = {chunk.chunk_id: chunk for chunk in selected_chunks}
                    citations = [
                        self._build_chunk_ref(selected_by_id[chunk_id])
                        for chunk_id in used_chunk_ids
                        if chunk_id in selected_by_id
                    ]
                    quote_by_chunk = {
                        quote.chunk_id: quote.quote for quote in evidence_quotes
                    }
                    self._attach_line_bboxes(
                        citations, pages_index, quote_by_chunk=quote_by_chunk
                    )
                    candidate_chunks = []
            latency_ms = int((perf_counter() - started_timer) * 1000)
            self.cache_service.set(
                cache_key,
                {
                    "task_type": task_type,
                    "model_name": model_result.model_name,
                    "route_tier": route_tier,
                    "route_model": route_model,
                    "route_reason": route_reason,
                    "response_detail_level": response_detail_level,
                    "result": result_content,
                    "outcome": outcome,
                    "context_strategy": context_strategy,
                    "retrieval_status": retrieval_status,
                    "retrieval_message": None,
                    "retrieval_applied": retrieval_applied,
                    "evidence_mode": evidence_mode,
                    "retrieved_chunk_count": retrieved_chunk_count,
                    "retrieved_pages": retrieved_pages,
                    "used_chunk_ids": used_chunk_ids,
                    "evidence_quotes": [quote.model_dump() for quote in evidence_quotes],
                    "citations": [citation.model_dump() for citation in citations],
                    "candidate_chunks": [chunk.model_dump() for chunk in candidate_chunks],
                    "source_chunks": [chunk.model_dump() for chunk in source_chunks],
                    "ask_evidence_retry_count": ask_evidence_retry_count,
                    "low_confidence_review": low_confidence_review,
                    "source_document_chars": model_result.source_document_chars,
                    "used_document_chars": model_result.used_document_chars,
                    "truncation_message": model_result.truncation_message,
                    "context_truncated": model_result.context_truncated,
                    "prompt_chars": model_result.prompt_chars,
                    "platform_request_id": platform_request_id,
                    "agent_iterations": agent_iterations,
                    "query_rewrites": query_rewrites,
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
                    route_tier=route_tier,
                    route_model=route_model,
                    route_reason=route_reason,
                    response_detail_level=response_detail_level,
                    file_id=file_id,
                    success=True,
                    outcome=outcome,
                    latency_ms=latency_ms,
                    platform_request_id=platform_request_id,
                    prompt_chars=model_result.prompt_chars,
                    output_chars=len(result_content),
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
                    evidence_mode=evidence_mode,
                    retrieved_chunk_count=retrieved_chunk_count,
                    context_truncated=model_result.context_truncated,
                    extra=(
                        {
                            "context_strategy": context_strategy,
                            "retrieved_pages": retrieved_pages,
                            "evidence_mode": evidence_mode,
                            "used_chunk_count": len(used_chunk_ids),
                            "evidence_quote_count": len(evidence_quotes),
                            "citation_count": len(citations),
                            "candidate_chunk_count": len(candidate_chunks),
                            "source_chunk_count": len(source_chunks),
                            "ask_evidence_retry_count": ask_evidence_retry_count,
                            "agent_iterations": agent_iterations,
                            "query_rewrites": query_rewrites,
                            "low_confidence_review": low_confidence_review,
                        }
                        if retrieved_pages or citations or candidate_chunks or source_chunks
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
                route_tier=route_tier,
                route_model=route_model,
                route_reason=route_reason,
                response_detail_level=response_detail_level,
                latency_ms=latency_ms,
                result=result_content,
                outcome=outcome,
                cache_hit=False,
                retrieval_status=retrieval_status,
                retrieval_message=None,
                retrieval_applied=retrieval_applied,
                evidence_mode=evidence_mode,
                retrieved_chunk_count=retrieved_chunk_count,
                retrieved_pages=retrieved_pages,
                used_chunk_ids=used_chunk_ids,
                evidence_quotes=evidence_quotes,
                citations=citations,
                candidate_chunks=candidate_chunks,
                source_chunks=source_chunks,
                source_document_chars=model_result.source_document_chars,
                used_document_chars=model_result.used_document_chars,
                truncation_message=model_result.truncation_message,
                context_truncated=model_result.context_truncated,
                token_usage=model_result.token_usage,
                platform_request_id=platform_request_id,
                agent_iterations=agent_iterations,
                query_rewrites=query_rewrites,
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
                    route_tier=route_tier,
                    route_model=route_model,
                    route_reason=route_reason,
                    response_detail_level=response_detail_level,
                    file_id=file_id if metadata or file_id else None,
                    success=False,
                    outcome="error",
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
                            "evidence_mode": evidence_mode,
                            "citation_count": len(citations),
                            "candidate_chunk_count": len(candidate_chunks),
                            "source_chunk_count": len(source_chunks),
                            **exc.details,
                        }
                        if retrieved_pages or citations or candidate_chunks or source_chunks
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

    def _build_chunk_ref(self, chunk) -> Citation:
        return Citation(
            chunk_id=chunk.chunk_id,
            page_numbers=chunk.page_numbers,
            snippet=self._build_display_snippet(chunk.text),
            bbox_regions=list(getattr(chunk, "bbox_regions", []) or []),
        )

    def _build_pages_index(
        self,
        file_id: str,
        *,
        access_token: str | None,
        session_id: str | None,
    ) -> dict[int, list[ParsedLine]]:
        try:
            structure = self.file_service.get_document_structure(
                file_id,
                access_token=access_token,
                session_id=session_id,
            )
        except Exception:
            return {}
        return {page.page_number: list(page.lines) for page in structure.pages}

    def _attach_line_bboxes(
        self,
        citations: list[Citation],
        pages_index: dict[int, list[ParsedLine]],
        *,
        quote_by_chunk: dict[str, str] | None = None,
    ) -> None:
        if not citations or not pages_index:
            return
        for citation in citations:
            text_candidates: list[str] = []
            if quote_by_chunk:
                quote = quote_by_chunk.get(citation.chunk_id)
                if quote:
                    text_candidates.append(quote)
            if citation.snippet:
                text_candidates.append(citation.snippet)

            matched: list = []
            for page_number in citation.page_numbers:
                lines = pages_index.get(page_number)
                if not lines:
                    continue
                for text in text_candidates:
                    result = match_snippet_to_line_bboxes(page_number, lines, text)
                    if result:
                        matched.extend(result)
                        break
            citation.bbox_regions = matched

    def _run_agentic_ask(
        self,
        *,
        chunked_document,
        selected_chunks: list[ParsedChunk],
        user_input: str | None,
        model_name_override: str | None,
        response_detail_level: ResponseDetailLevel,
        file_id: str | None = None,
    ) -> tuple[
        ModelResult,
        str,
        list[str],
        list[EvidenceQuote],
        int,
        bool,
        list[ParsedChunk],
        int,
        list[str],
    ]:
        """Agentic ask loop: retrieve -> answer + self-assess evidence sufficiency ->
        if the model judges the evidence insufficient and proposes a followup query,
        re-retrieve additional chunks (excluding ones already in context) and re-ask.

        Bounded to AGENTIC_ASK_MAX_ITERS model calls and AGENTIC_ASK_MAX_CHUNKS context
        chunks. The refusal/evidence contract is unchanged: a clean refusal still refuses,
        only substring-validated quotes count, and when the model never asks for more this
        behaves exactly like the previous single-context evidence retry.

        Returns the final (possibly expanded) chunk set so the caller can resolve citations
        against every chunk the model was actually shown, plus agentic telemetry.
        """
        accumulated: list[ParsedChunk] = list(selected_chunks)
        accumulated_ids = {chunk.chunk_id for chunk in accumulated}
        best_rank = -1
        best_result: tuple[ModelResult, str, list[str], list[EvidenceQuote], bool] | None = None
        performed_retry_count = 0
        agent_iterations = 0
        query_rewrites: list[str] = []
        pending_followup: str | None = None

        for attempt in range(self.AGENTIC_ASK_MAX_ITERS):
            if attempt > 0:
                performed_retry_count = attempt
                # Agentic re-retrieval: if the previous turn judged the evidence
                # insufficient and named a followup query, fetch additional chunks before
                # re-asking. Falls back to re-prompting the same context when no new
                # evidence is found (preserves the original retry semantics).
                if pending_followup and chunked_document is not None:
                    new_chunks = self.retrieval_service.retrieve(
                        pending_followup, chunked_document, file_id=file_id
                    )
                    added = [
                        chunk
                        for chunk in new_chunks
                        if chunk.chunk_id not in accumulated_ids
                    ]
                    if added:
                        query_rewrites.append(pending_followup)
                        for chunk in added:
                            if len(accumulated) >= self.AGENTIC_ASK_MAX_CHUNKS:
                                break
                            accumulated.append(chunk)
                            accumulated_ids.add(chunk.chunk_id)
                pending_followup = None

            agent_iterations = attempt + 1
            document_text = self._render_agentic_context(accumulated)
            current_user_input = (
                user_input
                if attempt == 0
                else self._build_ask_evidence_retry_input(user_input)
            )
            model_result = self.model_client.call_model(
                task_type="ask",
                document_text=document_text,
                user_input=current_user_input,
                model_name_override=model_name_override,
                response_detail_level=response_detail_level,
            )
            (
                result_content,
                used_chunk_ids,
                evidence_quotes,
                refused,
                followup_query,
                need_more,
            ) = self._extract_ask_evidence(model_result.content, accumulated)

            converged = bool(used_chunk_ids and evidence_quotes)
            pending_followup = followup_query if (need_more or not converged) else None

            if refused:
                if attempt + 1 < self.AGENTIC_ASK_MAX_ITERS:
                    best_result = (model_result, result_content, [], [], True)
                    continue
                return (
                    model_result,
                    result_content,
                    [],
                    [],
                    performed_retry_count,
                    True,
                    accumulated,
                    agent_iterations,
                    query_rewrites,
                )

            rank = 0
            if used_chunk_ids:
                rank = 1
            if used_chunk_ids and evidence_quotes:
                rank = 2

            if rank > best_rank:
                best_rank = rank
                best_result = (
                    model_result,
                    result_content,
                    used_chunk_ids,
                    evidence_quotes,
                    False,
                )

            if rank >= 2:
                break

        if best_result is None:
            raise RuntimeError("agentic ask produced no model result")

        model_result, result_content, used_chunk_ids, evidence_quotes, refused = best_result
        return (
            model_result,
            result_content,
            used_chunk_ids,
            evidence_quotes,
            performed_retry_count,
            refused,
            accumulated,
            agent_iterations,
            query_rewrites,
        )

    def _render_agentic_context(self, chunks: list[ParsedChunk]) -> str:
        return "\n\n".join(
            f"【Chunk {chunk.chunk_id} | Pages {','.join(str(page) for page in chunk.page_numbers)}】\n{chunk.text}"
            for chunk in chunks
        )

    def _build_ask_evidence_retry_input(self, user_input: str | None) -> str:
        base_question = (user_input or "请基于文档回答问题。").strip()
        retry_instruction = (
            "补充要求：这次必须只返回一个 JSON 对象，不要输出任何额外说明。"
            "系统已经检索到与问题相关的候选 chunk；请先逐条检查这些 chunk。"
            "只要 chunk 中存在可直接支持或可综合支持答案的原文片段，就不要拒答，"
            "而应返回 refused=false 并基于这些片段回答。"
            "回答语言必须跟随用户问题的主要语言；不要把英文问题默认翻译成中文回答。"
            "如果 chunk 明确说明某个字段未提供、不可恢复、没有例外或没有对应规则，"
            "且用户直接索要这个缺失字段的具体值，则返回 refused=true 并说明文档明确未提供该值。"
            "如果 chunk 显示存在互相冲突的信息且没有优先级规则，不要泛泛拒答；"
            "应返回 refused=false，说明存在冲突、无法唯一确定，并引用冲突依据。"
            "只有所有候选 chunk 都完全没有相关依据时，才允许 refused=true。"
            "used_chunk_ids 必须填写你实际使用的 chunk_id；"
            "evidence_quotes 至少返回 1 条；"
            "quote 必须从对应 chunk 原文连续逐字复制，不得改写、不得省略号、不得合并两段。"
        )
        return f"{base_question}\n\n{retry_instruction}"

    def _extract_ask_evidence(
        self,
        raw_content: str,
        selected_chunks: list[ParsedChunk],
    ) -> tuple[str, list[str], list[EvidenceQuote], bool, str | None, bool]:
        payload = self._extract_json_payload(raw_content)
        if not payload:
            return raw_content.strip(), [], [], False, None, False

        selected_by_id = {chunk.chunk_id: chunk for chunk in selected_chunks}
        allowed_chunk_ids = set(selected_by_id)
        answer = str(payload.get("answer") or "").strip() or raw_content.strip()
        used_chunk_ids = [
            str(item)
            for item in payload.get("used_chunk_ids", [])
            if str(item) in allowed_chunk_ids
        ]
        evidence_quotes = self._extract_validated_quotes(
            payload.get("evidence_quotes", []),
            used_chunk_ids,
            selected_by_id,
        )
        refused = bool(payload.get("refused"))
        followup_query = str(payload.get("followup_query") or "").strip() or None
        need_more = bool(payload.get("need_more"))
        return answer, used_chunk_ids, evidence_quotes, refused, followup_query, need_more

    def _extract_validated_quotes(
        self,
        raw_quotes: list,
        used_chunk_ids: list[str],
        selected_by_id: dict[str, ParsedChunk],
    ) -> list[EvidenceQuote]:
        if not used_chunk_ids:
            return []

        normalized_chunks = {
            chunk_id: self._normalize_quote_text(selected_by_id[chunk_id].text)
            for chunk_id in used_chunk_ids
            if chunk_id in selected_by_id
        }

        validated: list[EvidenceQuote] = []
        for item in raw_quotes[:5]:
            chunk_id, quote = self._coerce_quote_item(item, used_chunk_ids)
            if not chunk_id or not quote:
                continue
            normalized_quote = self._normalize_quote_text(quote)
            if not normalized_quote:
                continue
            if normalized_quote not in normalized_chunks.get(chunk_id, ""):
                continue
            validated.append(EvidenceQuote(chunk_id=chunk_id, quote=quote.strip()))
            if len(validated) >= 3:
                break
        return validated

    def _coerce_quote_item(
        self,
        item: object,
        used_chunk_ids: list[str],
    ) -> tuple[str | None, str | None]:
        if isinstance(item, dict):
            chunk_id = str(item.get("chunk_id") or "").strip()
            quote = str(item.get("quote") or "").strip()
            if chunk_id in used_chunk_ids and quote:
                return chunk_id, quote
            return None, None
        return None, None

    def _normalize_quote_text(self, text: str) -> str:
        normalized = text.replace("\x00", "")
        normalized = re.sub(r"\s+", "", normalized)
        normalized = re.sub(
            r"[，。、！？,\.!\?;；：:（）()\-\u2013\u2014\u2018\u2019\u201c\u201d\"']",
            "",
            normalized,
        )
        return normalized.strip()

    def _extract_json_payload(self, raw_content: str) -> dict | None:
        candidate = raw_content.strip()
        if candidate.startswith("```"):
            candidate = re.sub(r"^```(?:json)?\s*|\s*```$", "", candidate, flags=re.DOTALL).strip()

        for value in (candidate, self._extract_braced_object(candidate)):
            if not value:
                continue
            try:
                payload = json.loads(value)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict):
                return payload
        return None

    def _extract_braced_object(self, content: str) -> str | None:
        start = content.find("{")
        end = content.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return None
        return content[start : end + 1]

    def _select_display_chunks(
        self,
        chunks: list[ParsedChunk],
        *,
        limit: int,
    ) -> list[ParsedChunk]:
        if len(chunks) <= limit:
            return chunks

        scored = [
            (self._score_display_chunk(chunk.text, index=index), index, chunk)
            for index, chunk in enumerate(chunks)
        ]
        scored.sort(
            key=lambda item: (
                -item[0],
                item[2].page_numbers[0] if item[2].page_numbers else 0,
                item[1],
            )
        )

        selected: list[tuple[int, ParsedChunk]] = []
        used_pages: set[int] = set()
        for _, index, chunk in scored:
            page_set = set(chunk.page_numbers)
            if used_pages & page_set and len(selected) < limit - 1:
                continue
            selected.append((index, chunk))
            used_pages.update(page_set)
            if len(selected) >= limit:
                break

        if len(selected) < limit:
            existing_ids = {chunk.chunk_id for _, chunk in selected}
            for _, index, chunk in scored:
                if chunk.chunk_id in existing_ids:
                    continue
                selected.append((index, chunk))
                if len(selected) >= limit:
                    break

        selected.sort(key=lambda item: item[0])
        return [chunk for _, chunk in selected]

    def _build_display_snippet(self, text: str, *, limit: int = 220) -> str:
        cleaned_lines: list[str] = []
        for raw_line in text.replace("\x00", "").splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if self._is_display_artifact(line):
                continue
            normalized = self._normalize_display_line(line)
            if normalized:
                cleaned_lines.append(normalized)

        snippet = " ".join(cleaned_lines)
        if not snippet:
            snippet = self._normalize_display_line(text)

        if len(snippet) <= limit:
            return snippet
        return snippet[:limit].rstrip() + "..."

    def _score_display_chunk(self, text: str, *, index: int = 0) -> float:
        snippet = self._build_display_snippet(text, limit=280)
        lowered = snippet.lower()
        cjk_count = sum("\u4e00" <= char <= "\u9fff" for char in snippet)
        digit_count = sum(char.isdigit() for char in snippet)
        alpha_count = sum(char.isalpha() for char in snippet)

        score = 0.0
        score += min(len(snippet), 220) / 36
        score += min(cjk_count, 120) / 28

        if index == 0:
            score += 1.5

        for keyword in ("摘要", "引言", "研究", "方法", "实验", "结果", "结论", "讨论"):
            if keyword in snippet:
                score += 2.0

        for keyword in ("abstract", "introduction", "method", "result", "conclusion"):
            if keyword in lowered:
                score += 1.2

        noisy_markers = (
            "table",
            "workflow",
            "goal:",
            "option",
            "answer",
            "thought",
            "prompt engineering",
            "@mail",
        )
        if any(marker in lowered for marker in noisy_markers):
            score -= 7.5

        if "第" in snippet and "页" in snippet and digit_count >= 4:
            score -= 4.0

        if digit_count >= max(10, len(snippet) // 5):
            score -= 3.0

        if alpha_count > cjk_count and alpha_count >= 40:
            score -= 2.5

        if re.search(r"([\u4e00-\u9fff])(?:\s+\1){1,}", text):
            score -= 2.0

        return score

    def _normalize_display_line(self, text: str) -> str:
        text = text.replace("\x00", " ")
        text = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", text)
        text = re.sub(r"([\u4e00-\u9fff])\1{2,}", r"\1", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _is_display_artifact(self, line: str) -> bool:
        normalized = re.sub(r"\s+", "", line).lower()
        if not normalized:
            return True

        artifact_patterns = (
            "第二十三届中国计算语言学大会论文集",
            "中国中文信息学会计算语言学专业委员会",
            "creativecommons attribution 4.0 international license",
            "ccl2024",
            "卷3：评测报告",
        )
        if any(re.sub(r"\s+", "", pattern).lower() in normalized for pattern in artifact_patterns):
            return True

        if re.fullmatch(r"[\[\]()（）\-—·,.，。:：;；/\\\d\s]+", line):
            return True

        digit_count = sum(char.isdigit() for char in line)
        alpha_count = sum(char.isalpha() for char in line)
        cjk_count = sum("\u4e00" <= char <= "\u9fff" for char in line)
        if digit_count >= 8 and cjk_count <= 4 and alpha_count <= 18:
            return True

        if digit_count >= max(6, len(line) // 3) and line.count(" ") >= 4:
            return True

        return False
