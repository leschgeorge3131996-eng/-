from __future__ import annotations

import json
import shutil
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

import pytest

from backend.app.core.exceptions import ForbiddenError, NotFoundError, ParseError

from backend.app.core.config import Settings
from backend.app.schemas.document import ChunkedDocument, ParsedDocument, ParsedPage, ParsedChunk
from backend.app.schemas.log import CallLogEntry
from backend.app.schemas.task import ResponseDetailLevel
from backend.app.services.chunk_service import ChunkService
from backend.app.services.file_service import FileService
from backend.app.services.log_service import LogService
from backend.app.services.model_client import ModelClient
from backend.app.services.context_planner import PlannedContext
from backend.app.services.retrieval_service import RetrievalService
from backend.app.services.task_service import TaskService
from backend.app.services.document_parser import DocumentParser


def make_workspace() -> Path:
    root = Path.cwd() / ".test_tmp" / uuid4().hex
    root.mkdir(parents=True, exist_ok=True)
    return root


def cleanup_workspace(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)


def build_settings(
    tmp_root: Path,
    *,
    model_lite: str = "",
    model_pro: str = "",
    route_upgrade_chars: int = 12000,
) -> Settings:
    data_dir = tmp_root / "data"
    uploads_dir = data_dir / "uploads"
    parsed_dir = data_dir / "parsed"
    logs_dir = data_dir / "logs"
    cache_dir = data_dir / "cache"
    settings = Settings(
        project_root=tmp_root,
        app_name="test-app",
        app_env="test",
        api_prefix="/api",
        cors_origins=["http://localhost:5173"],
        log_level="INFO",
        max_upload_mb=5,
        max_document_chars=10000,
        request_timeout_seconds=30,
        document_retention_hours=72,
        session_retention_hours=168,
        session_cookie_name="yandatong_session",
        session_cookie_secure=False,
        session_cookie_samesite="lax",
        alpha_invite_codes=["invite-123"],
        demo_mode=False,
        data_dir=data_dir,
        uploads_dir=uploads_dir,
        parsed_dir=parsed_dir,
        sessions_dir=data_dir / "sessions",
        logs_dir=logs_dir,
        cache_dir=cache_dir,
        model_provider="mock",
        use_mock_model=True,
        wuqiong_base_url="",
        wuqiong_api_key="",
        model_lite=model_lite,
        model_pro=model_pro,
        model_qa="mock-qa",
        model_summary="mock-summary",
        model_outline="mock-outline",
        route_upgrade_chars=route_upgrade_chars,
    )
    settings.ensure_directories()
    return settings


def test_save_upload_and_load_text() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        service = FileService(settings=settings)

        result = service.save_upload("demo.txt", "first paragraph\nsecond paragraph".encode("utf-8"))
        text = service.get_document_text(result.file_id, access_token=result.access_token)
        structure = service.get_document_structure(result.file_id, access_token=result.access_token)
        chunks = service.get_document_chunks(result.file_id, access_token=result.access_token)

        assert result.parse_status == "parsed"
        assert result.text_chars > 0
        assert result.page_count == 1
        assert result.chunk_count >= 1
        assert result.document_fingerprint
        assert structure.page_count == 1
        assert structure.pages[0].text == text
        assert chunks.chunk_count >= 1
        assert "first paragraph" in text
    finally:
        cleanup_workspace(workspace)


def test_file_service_requires_access_token_for_new_documents() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        service = FileService(settings=settings)
        result = service.save_upload(
            "demo.txt",
            "测试内容".encode("utf-8"),
            owner_session_id="owner-session",
        )

        with pytest.raises(ForbiddenError):
            service.get_document_text(result.file_id)

        with pytest.raises(ForbiddenError):
            service.get_document_text(
                result.file_id,
                access_token=result.access_token,
                session_id="other-session",
            )

        assert service.get_document_text(
            result.file_id,
            access_token=result.access_token,
            session_id="owner-session",
        )
    finally:
        cleanup_workspace(workspace)


def test_file_service_delete_document_removes_related_files() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        service = FileService(settings=settings)
        result = service.save_upload("demo.txt", "测试内容".encode("utf-8"))

        deleted = service.delete_document(result.file_id, access_token=result.access_token)

        assert deleted.file_id == result.file_id
        with pytest.raises(NotFoundError):
            service.get_document_metadata(result.file_id, access_token=result.access_token)
    finally:
        cleanup_workspace(workspace)


def test_file_service_cleanup_expired_documents_removes_old_files() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        service = FileService(settings=settings)
        result = service.save_upload("demo.txt", "测试内容".encode("utf-8"))

        deleted_ids = service.cleanup_expired_documents(
            now=(
                datetime.fromisoformat(result.expires_at) + timedelta(seconds=1)
            )
        )

        assert deleted_ids == [result.file_id]
        with pytest.raises(NotFoundError):
            service.get_document_metadata(result.file_id, access_token=result.access_token)
    finally:
        cleanup_workspace(workspace)


def test_task_service_writes_log() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        log_service = LogService(settings=settings)
        model_client = ModelClient(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=model_client,
            log_service=log_service,
        )

        upload = file_service.save_upload(
            "paper.md",
            "# Title\n\nThis is a test document.\n\nIt includes background and method notes.".encode("utf-8"),
        )
        result = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="璇风獊鍑哄垱鏂扮偣",
            response_detail_level="detailed",
        )
        logs = log_service.list_logs(limit=10)

        assert result.task_type == "summary"
        assert result.response_detail_level == "detailed"
        assert result.request_id
        assert logs
        assert logs[0]["success"] is True
        assert logs[0]["task_type"] == "summary"
        assert logs[0]["response_detail_level"] == "detailed"
    finally:
        cleanup_workspace(workspace)


class BrokenPdfParser(DocumentParser):
    def extract_text(self, file_path: Path) -> str:
        raise RuntimeError("broken parser")


class FailingLogService(LogService):
    def write_log(self, entry: CallLogEntry) -> None:
        raise OSError("disk full")


class CountingModelClient(ModelClient):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings=settings)
        self.call_count = 0

    def call_model(
        self,
        task_type: str,
        document_text: str,
        user_input: str | None = None,
        model_name_override: str | None = None,
        response_detail_level: ResponseDetailLevel = "balanced",
    ):
        self.call_count += 1
        return super().call_model(
            task_type,
            document_text,
            user_input,
            model_name_override=model_name_override,
            response_detail_level=response_detail_level,
        )


class RecordingModelClient(ModelClient):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings=settings)
        self.last_document_text = ""
        self.last_task_type = ""
        self.last_response_detail_level: ResponseDetailLevel = "balanced"

    def call_model(
        self,
        task_type: str,
        document_text: str,
        user_input: str | None = None,
        model_name_override: str | None = None,
        response_detail_level: ResponseDetailLevel = "balanced",
    ):
        self.last_task_type = task_type
        self.last_document_text = document_text
        self.last_response_detail_level = response_detail_level
        return super().call_model(
            task_type,
            document_text,
            user_input,
            model_name_override=model_name_override,
            response_detail_level=response_detail_level,
        )


class PlainTextAskModelClient(ModelClient):
    def call_model(
        self,
        task_type: str,
        document_text: str,
        user_input: str | None = None,
        model_name_override: str | None = None,
        response_detail_level: ResponseDetailLevel = "balanced",
    ):
        if task_type == "ask":
            plain_text_answer = "Plain text answer without JSON."
            return super().call_model(
                task_type,
                document_text,
                user_input,
                model_name_override=model_name_override,
                response_detail_level=response_detail_level,
            ).model_copy(
                update={
                    "content": plain_text_answer,
                    "output_chars": len(plain_text_answer),
                }
            )
        return super().call_model(
            task_type,
            document_text,
            user_input,
            model_name_override=model_name_override,
            response_detail_level=response_detail_level,
        )


class RetryThenStructuredAskModelClient(ModelClient):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings=settings)
        self.ask_call_count = 0

    def call_model(
        self,
        task_type: str,
        document_text: str,
        user_input: str | None = None,
        model_name_override: str | None = None,
        response_detail_level: ResponseDetailLevel = "balanced",
    ):
        if task_type == "ask":
            self.ask_call_count += 1
            if self.ask_call_count == 1:
                plain_text_answer = "Plain text answer without JSON."
                return super().call_model(
                    task_type,
                    document_text,
                    user_input,
                    model_name_override=model_name_override,
                    response_detail_level=response_detail_level,
                ).model_copy(
                    update={
                        "content": plain_text_answer,
                        "output_chars": len(plain_text_answer),
                    }
                )
        return super().call_model(
            task_type,
            document_text,
            user_input,
            model_name_override=model_name_override,
            response_detail_level=response_detail_level,
        )


class RefuseThenStructuredAskModelClient(ModelClient):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings=settings)
        self.ask_call_count = 0

    def call_model(
        self,
        task_type: str,
        document_text: str,
        user_input: str | None = None,
        model_name_override: str | None = None,
        response_detail_level: ResponseDetailLevel = "balanced",
    ):
        if task_type == "ask":
            self.ask_call_count += 1
            base_result = super().call_model(
                task_type,
                document_text,
                user_input,
                model_name_override=model_name_override,
                response_detail_level=response_detail_level,
            )
            if self.ask_call_count == 1:
                refused_payload = (
                    '{"refused":true,"answer":"无法从文档中找到相关依据回答此问题",'
                    '"used_chunk_ids":[],"evidence_quotes":[]}'
                )
                return base_result.model_copy(
                    update={
                        "content": refused_payload,
                        "output_chars": len(refused_payload),
                    }
                )
            return base_result
        return super().call_model(
            task_type,
            document_text,
            user_input,
            model_name_override=model_name_override,
            response_detail_level=response_detail_level,
        )


class FixedLowConfidencePlanner:
    def __init__(self, selected_chunks: list[ParsedChunk]) -> None:
        self.selected_chunks = selected_chunks

    def plan(self, **_kwargs) -> PlannedContext:
        context = "\n\n".join(
            f"【Chunk {chunk.chunk_id} | Pages {','.join(str(page) for page in chunk.page_numbers)}】\n{chunk.text}"
            for chunk in self.selected_chunks
        )
        return PlannedContext(
            strategy="retrieval_topk",
            document_text=context,
            selected_chunks=self.selected_chunks,
            retrieval_confident=False,
        )


class NoEvidenceAskModelClient(ModelClient):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings=settings)
        self.ask_call_count = 0

    def call_model(
        self,
        task_type: str,
        document_text: str,
        user_input: str | None = None,
        model_name_override: str | None = None,
        response_detail_level: ResponseDetailLevel = "balanced",
    ):
        if task_type == "ask":
            self.ask_call_count += 1
            payload = (
                '{"refused":false,"answer":"Unsupported answer without validated evidence.",'
                '"used_chunk_ids":[],"evidence_quotes":[]}'
            )
            return super().call_model(
                task_type,
                document_text,
                user_input,
                model_name_override=model_name_override,
                response_detail_level=response_detail_level,
            ).model_copy(
                update={
                    "content": payload,
                    "output_chars": len(payload),
                }
            )
        return super().call_model(
            task_type,
            document_text,
            user_input,
            model_name_override=model_name_override,
            response_detail_level=response_detail_level,
        )


def test_parse_error_is_normalized() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        service = FileService(settings=settings, parser=BrokenPdfParser())

        with pytest.raises(ParseError):
            service.save_upload("bad.pdf", b"%PDF-1.4 fake")
    finally:
        cleanup_workspace(workspace)


def test_document_parser_strips_surrogate_codepoints() -> None:
    parser = DocumentParser()

    normalized = parser._normalize_text("姝ｅ父鏂囨湰\ud835淇濈暀閮ㄥ垎")

    assert normalized == "姝ｅ父鏂囨湰淇濈暀閮ㄥ垎"


def test_task_service_still_returns_when_log_write_fails() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=ModelClient(settings=settings),
            log_service=FailingLogService(settings=settings),
        )
        upload = file_service.save_upload("demo.txt", "A short test passage.".encode("utf-8"))

        result = task_service.run_task(
            task_type="ask",
            endpoint="/api/ask",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="What does this passage say?",
        )

        assert result.result
        assert result.task_type == "ask"
    finally:
        cleanup_workspace(workspace)


def test_log_service_skips_malformed_lines() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        log_service = LogService(settings=settings)
        log_service.log_file.write_text(
            '{"request_id":"ok","timestamp":"now","endpoint":"/api/ask","task_type":"ask","model_name":"m","success":true,"latency_ms":1,"prompt_chars":1,"output_chars":1}\n'
            '{bad json line}\n',
            encoding="utf-8",
        )

        logs = log_service.list_logs(limit=10)

        assert len(logs) == 1
        assert logs[0]["request_id"] == "ok"
    finally:
        cleanup_workspace(workspace)


def test_log_service_summary_aggregates_metrics() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        log_service = LogService(settings=settings)
        log_service.log_file.write_text(
            "\n".join(
                [
                    '{"request_id":"1","timestamp":"2026-04-15T01:00:00+00:00","endpoint":"/api/summary","task_type":"summary","model_name":"m1","route_tier":"lite","success":true,"outcome":"answered","latency_ms":100,"prompt_chars":10,"output_chars":20,"token_total":30,"cache_hit":false,"retrieval_status":"coverage","extra":{"citation_count":2}}',
                    '{"request_id":"2","timestamp":"2026-04-15T01:01:00+00:00","endpoint":"/api/ask","task_type":"ask","model_name":"m1","route_tier":"none","response_detail_level":"concise","success":true,"outcome":"refused","latency_ms":400,"prompt_chars":10,"output_chars":15,"token_total":0,"cache_hit":false,"retrieval_status":"no_match","extra":{"citation_count":0}}',
                    '{"request_id":"3","timestamp":"2026-04-15T01:02:00+00:00","endpoint":"/api/summary","task_type":"summary","model_name":"m2","route_tier":"pro","response_detail_level":"detailed","success":false,"outcome":"error","latency_ms":200,"prompt_chars":10,"output_chars":0,"token_total":40,"cache_hit":true,"retrieval_applied":true,"retrieval_status":"matched","error_type":"MODEL_SERVICE_ERROR","extra":{"citation_count":1}}',
                    "{bad json line}",
                ]
            ),
            encoding="utf-8",
        )

        summary = log_service.summarize_logs()

        assert summary["total_requests"] == 3
        assert summary["success_count"] == 2
        assert summary["failure_count"] == 1
        assert summary["cache_hit_count"] == 1
        assert summary["retrieval_applied_count"] == 1
        assert summary["citation_count_sum"] == 3
        assert summary["answered_count"] == 1
        assert summary["refused_count"] == 1
        assert summary["error_count"] == 1
        assert summary["token_total_sum"] == 70
        assert summary["by_task"]["summary"] == 2
        assert summary["by_task"]["ask"] == 1
        assert summary["by_model"]["m1"] == 2
        assert summary["by_model"]["m2"] == 1
        assert summary["by_outcome"]["answered"] == 1
        assert summary["by_outcome"]["refused"] == 1
        assert summary["by_outcome"]["error"] == 1
        assert summary["by_response_detail_level"]["concise"] == 1
        assert summary["by_response_detail_level"]["detailed"] == 1
        assert summary["by_route_tier"]["lite"] == 1
        assert summary["by_route_tier"]["none"] == 1
        assert summary["by_route_tier"]["pro"] == 1
        assert summary["by_retrieval_status"]["coverage"] == 1
        assert summary["by_retrieval_status"]["no_match"] == 1
        assert summary["by_retrieval_status"]["matched"] == 1
        assert summary["error_types"]["MODEL_SERVICE_ERROR"] == 1
    finally:
        cleanup_workspace(workspace)


def test_task_service_uses_cache_for_same_request() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        log_service = LogService(settings=settings)
        model_client = CountingModelClient(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=model_client,
            log_service=log_service,
        )
        upload = file_service.save_upload("demo.txt", "缂撳瓨娴嬭瘯鍐呭".encode("utf-8"))

        first = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="璇锋€荤粨",
            response_detail_level="concise",
        )
        second = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="璇锋€荤粨",
            response_detail_level="concise",
        )

        assert first.cache_hit is False
        assert second.cache_hit is True
        assert model_client.call_count == 1
        assert first.result == second.result
    finally:
        cleanup_workspace(workspace)


def test_task_service_separates_cache_by_response_detail_level() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        log_service = LogService(settings=settings)
        model_client = CountingModelClient(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=model_client,
            log_service=log_service,
        )
        upload = file_service.save_upload("demo.txt", "缂撳瓨娴嬭瘯鍐呭".encode("utf-8"))

        concise = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="璇锋€荤粨",
            response_detail_level="concise",
        )
        detailed = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="璇锋€荤粨",
            response_detail_level="detailed",
        )

        assert concise.response_detail_level == "concise"
        assert detailed.response_detail_level == "detailed"
        assert model_client.call_count == 2
    finally:
        cleanup_workspace(workspace)


def test_task_service_applies_retrieval_for_ask() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=ModelClient(settings=settings),
            log_service=LogService(settings=settings),
        )
        upload = file_service.save_upload(
            "retrieval.md",
            (
                "# Background\n\nThis section only contains background information.\n\n"
                "# Goal\n\nThe first-phase goal is to support upload, summary, ask, and outline generation."
            ).encode("utf-8"),
        )

        result = task_service.run_task(
            task_type="ask",
            endpoint="/api/ask",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="What is the first-phase goal?",
        )

        assert result.evidence_mode == "declared"
        assert result.retrieval_applied is True
        assert result.retrieved_chunk_count >= 1
        assert result.retrieved_pages == [1]
        assert len(result.citations) >= 1
        assert len(result.used_chunk_ids) >= 1
        assert len(result.evidence_quotes) >= 1
        assert result.evidence_quotes[0].chunk_id in result.used_chunk_ids
        assert result.citations[0].page_numbers == [1]
        assert result.candidate_chunks == []
        assert result.source_chunks == []
    finally:
        cleanup_workspace(workspace)


def test_ask_citations_follow_model_declared_chunk_ids() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=ModelClient(settings=settings),
            log_service=LogService(settings=settings),
        )
        upload = file_service.save_upload(
            "evidence.md",
            (
                "# Background\n\nThis is background context.\n\n"
                "# Goal\n\nThe first-phase goal is to support upload, summary, ask, and outline generation.\n\n"
                "# Method\n\nThis section explains the method."
            ).encode("utf-8"),
        )

        result = task_service.run_task(
            task_type="ask",
            endpoint="/api/ask",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="What is the first-phase goal?",
        )

        assert result.used_chunk_ids
        assert {citation.chunk_id for citation in result.citations}.issubset(set(result.used_chunk_ids))
    finally:
        cleanup_workspace(workspace)


def test_ask_plain_text_response_does_not_fallback_to_candidate_citations() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=PlainTextAskModelClient(settings=settings),
            log_service=LogService(settings=settings),
        )
        upload = file_service.save_upload(
            "plain_text.md",
            "# Goal\n\nThe first-phase goal is to support upload, summary, ask, and outline generation.".encode("utf-8"),
        )

        result = task_service.run_task(
            task_type="ask",
            endpoint="/api/ask",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="What is the first-phase goal?",
        )

        assert result.result == "Plain text answer without JSON."
        assert result.evidence_mode == "candidate"
        assert result.used_chunk_ids == []
        assert result.evidence_quotes == []
        assert result.citations == []
        assert len(result.candidate_chunks) >= 1
    finally:
        cleanup_workspace(workspace)


def test_ask_retries_once_when_structured_evidence_is_missing() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        model_client = RetryThenStructuredAskModelClient(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=model_client,
            log_service=LogService(settings=settings),
        )
        upload = file_service.save_upload(
            "retry.md",
            "# Goal\n\nThe first-phase goal is to support upload, summary, ask, and outline generation.".encode("utf-8"),
        )

        result = task_service.run_task(
            task_type="ask",
            endpoint="/api/ask",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="What is the first-phase goal?",
        )

        assert model_client.ask_call_count == 2
        assert result.evidence_mode == "declared"
        assert result.used_chunk_ids
        assert result.evidence_quotes
        assert result.citations
        assert result.candidate_chunks == []
    finally:
        cleanup_workspace(workspace)


def test_ask_retries_once_when_model_refuses_despite_retrieved_chunks() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        model_client = RefuseThenStructuredAskModelClient(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=model_client,
            log_service=LogService(settings=settings),
        )
        upload = file_service.save_upload(
            "retry-refusal.md",
            "# Goal\n\nThe first-phase goal is to support upload, summary, ask, and outline generation.".encode("utf-8"),
        )

        result = task_service.run_task(
            task_type="ask",
            endpoint="/api/ask",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="What is the first-phase goal?",
        )

        assert model_client.ask_call_count == 2
        assert result.outcome == "answered"
        assert result.route_reason != "llm_refused"
        assert result.evidence_mode == "declared"
        assert result.used_chunk_ids
        assert result.evidence_quotes
        assert result.citations
    finally:
        cleanup_workspace(workspace)


def test_low_confidence_ask_candidates_are_reviewed_by_model() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        upload = file_service.save_upload(
            "low-confidence.md",
            "# Goal\n\nThe first-phase goal is to support evidence-backed PDF question answering.".encode("utf-8"),
        )
        selected_chunk = file_service.get_document_chunks(
            upload.file_id,
            access_token=upload.access_token,
        ).chunks[0]
        task_service = TaskService(
            file_service=file_service,
            model_client=ModelClient(settings=settings),
            log_service=LogService(settings=settings),
            context_planner=FixedLowConfidencePlanner([selected_chunk]),
        )

        result = task_service.run_task(
            task_type="ask",
            endpoint="/api/ask",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="What is the goal?",
        )

        assert result.outcome == "answered"
        assert result.model_name != "retrieval_gate"
        assert result.retrieval_status == "low_confidence"
        assert result.retrieval_applied is True
        assert result.evidence_mode == "declared"
        assert result.used_chunk_ids
        assert result.evidence_quotes
        assert result.citations
        assert result.candidate_chunks == []
    finally:
        cleanup_workspace(workspace)


def test_low_confidence_ask_refuses_when_model_returns_no_valid_evidence() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        model_client = NoEvidenceAskModelClient(settings=settings)
        upload = file_service.save_upload(
            "low-confidence-no-evidence.md",
            "# Goal\n\nThe first-phase goal is to support evidence-backed PDF question answering.".encode("utf-8"),
        )
        selected_chunk = file_service.get_document_chunks(
            upload.file_id,
            access_token=upload.access_token,
        ).chunks[0]
        task_service = TaskService(
            file_service=file_service,
            model_client=model_client,
            log_service=LogService(settings=settings),
            context_planner=FixedLowConfidencePlanner([selected_chunk]),
        )

        result = task_service.run_task(
            task_type="ask",
            endpoint="/api/ask",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="What is the goal?",
        )

        assert model_client.ask_call_count == 2
        assert result.outcome == "refused"
        assert result.route_reason == "llm_refused"
        assert result.retrieval_status == "low_confidence"
        assert result.retrieval_applied is True
        assert result.evidence_mode == "none"
        assert result.retrieval_message
        assert result.used_chunk_ids == []
        assert result.evidence_quotes == []
        assert result.citations == []
        assert len(result.candidate_chunks) == 1
    finally:
        cleanup_workspace(workspace)


def test_task_service_avoids_fake_citations_on_retrieval_miss() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=ModelClient(settings=settings),
            log_service=LogService(settings=settings),
        )
        upload = file_service.save_upload(
            "miss.md",
            "# Document\n\nThis text only discusses background and project goals.".encode("utf-8"),
        )

        result = task_service.run_task(
            task_type="ask",
            endpoint="/api/ask",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="A completely unrelated astronomy question",
        )

        assert result.outcome == "refused"
        assert result.evidence_mode == "none"
        assert result.retrieval_status == "no_match"
        assert result.retrieval_message
        assert result.retrieval_applied is False
        assert result.retrieved_chunk_count == 0
        assert result.citations == []
    finally:
        cleanup_workspace(workspace)


def test_task_service_answers_metadata_name_question_without_keyword_overlap() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=ModelClient(settings=settings),
            log_service=LogService(settings=settings),
        )
        upload = file_service.save_upload(
            "research_brief.md",
            (
                "# 项目简介\n\n"
                "研答通是一款面向科研与智能办公场景的个人智能文档助理。\n"
                "第一阶段目标是支持用户上传文档，完成摘要、问答和提纲生成。"
            ).encode("utf-8"),
        )

        result = task_service.run_task(
            task_type="ask",
            endpoint="/api/ask",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="这个产品的名字是什么？",
        )

        assert result.outcome == "answered"
        assert result.retrieval_status == "matched"
        assert result.evidence_mode == "declared"
        assert "研答通" in result.result
        assert result.citations
        assert result.citations[0].page_numbers == [1]
    finally:
        cleanup_workspace(workspace)


def test_summary_uses_chunk_coverage_context() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        model_client = RecordingModelClient(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=model_client,
            log_service=LogService(settings=settings),
        )
        upload = file_service.save_upload(
            "coverage.md",
            (
                "# Section One\nSection one content.\n"
                "# Section Two\nSection two content.\n"
                "# Section Three\nSection three content.\n"
                "# Section Four\nSection four content.\n"
                "# Section Five\nSection five content.\n"
                "# Section Six\nSection six content."
            ).encode("utf-8"),
        )

        result = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="Please summarize the document.",
        )

        assert result.task_type == "summary"
        assert "【Chunk" in model_client.last_document_text
        assert result.citations == []
        assert len(result.source_chunks) >= 1
    finally:
        cleanup_workspace(workspace)


def test_summary_planner_responds_to_instruction_intent() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        model_client = RecordingModelClient(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=model_client,
            log_service=LogService(settings=settings),
        )
        upload = file_service.save_upload(
            "intent.md",
            (
                "# Background\n\n"
                + ("This section explains the research background. " * 80)
                + "\n\n# Dataset\n\n"
                + ("This section describes the dataset construction and labels. " * 80)
                + "\n\n# Method\n\n"
                + ("This section focuses on the method design and implementation. " * 80)
                + "\n\n# Ablation Study\n\n"
                + ("This section explains the ablation setup and comparisons. " * 80)
                + "\n\n# Experiment Results\n\n"
                + ("This section highlights the experiment results and performance. " * 80)
                + "\n\n# Error Analysis\n\n"
                + ("This section analyzes model errors and failure cases. " * 80)
                + "\n\n# Conclusion\n\n"
                + ("This section gives the final conclusion. " * 50)
                + "\n\n# Appendix\n\n"
                + ("This section contains supplementary notes and appendix material. " * 60)
            ).encode("utf-8"),
        )

        task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="Focus on the experiment results.",
        )
        experiment_text = model_client.last_document_text

        task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="Focus on the method section.",
        )
        method_text = model_client.last_document_text

        assert "experiment results" in experiment_text.lower()
        assert "method design" in method_text.lower()
        assert experiment_text != method_text
    finally:
        cleanup_workspace(workspace)


def test_summary_source_chunks_are_cleaned_for_display() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=ModelClient(settings=settings),
            log_service=LogService(settings=settings),
        )
        upload = file_service.save_upload(
            "cleaning.md",
            (
                "CCL2024\n"
                "Creative Commons Attribution 4.0 International License\n\n"
                "This is a normal research explanation that should remain in the source snippet."
            ).encode("utf-8"),
        )

        result = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="璇锋€荤粨",
        )

        assert result.source_chunks
        snippet = result.source_chunks[0].snippet
        assert "CCL2024" not in snippet
        assert "Creative Commons Attribution 4.0 International License" not in snippet
        assert "normal research explanation" in snippet
    finally:
        cleanup_workspace(workspace)


def test_task_service_uses_task_tier_route_when_configured() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(
            workspace,
            model_lite="lite-model",
            model_pro="pro-model",
        )
        file_service = FileService(settings=settings)
        model_client = RecordingModelClient(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=model_client,
            log_service=LogService(settings=settings),
        )
        upload = file_service.save_upload("demo.md", "# 鏍囬\n\n鍐呭".encode("utf-8"))

        summary_result = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="璇锋€荤粨",
        )
        ask_result = task_service.run_task(
            task_type="ask",
            endpoint="/api/ask",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="鏍囬鏄粈涔堬紵",
        )

        assert summary_result.route_tier == "lite"
        assert summary_result.route_model == "lite-model"
        assert ask_result.route_tier == "pro"
        assert ask_result.route_model == "pro-model"
    finally:
        cleanup_workspace(workspace)


def test_chunk_ids_are_stable_for_same_text() -> None:
    parsed_document = ParsedDocument(
        file_type="md",
        text="# Title\n\nFirst paragraph\nSecond paragraph",
        page_count=1,
        pages=[
            ParsedPage(
                page_number=1,
                text="# Title\n\nFirst paragraph\nSecond paragraph",
                char_count=len("# Title\n\nFirst paragraph\nSecond paragraph"),
            )
        ],
    )
    service = ChunkService()

    first = service.build_chunks(parsed_document)
    second = service.build_chunks(parsed_document)

    assert [chunk.chunk_id for chunk in first.chunks] == [chunk.chunk_id for chunk in second.chunks]


def test_chunk_ids_do_not_collide_for_repeated_same_page_text() -> None:
    parsed_document = ParsedDocument(
        file_type="md",
        text="First paragraph\nFirst paragraph\nSecond paragraph",
        page_count=1,
        pages=[
            ParsedPage(
                page_number=1,
                text="First paragraph\nFirst paragraph\nSecond paragraph",
                char_count=len("First paragraph\nFirst paragraph\nSecond paragraph"),
            )
        ],
    )
    service = ChunkService(target_chunk_chars=3, min_chunk_chars=1, long_text_step=3)

    chunked = service.build_chunks(parsed_document)

    assert len({chunk.chunk_id for chunk in chunked.chunks}) == chunked.chunk_count


def test_chunk_service_assigns_stable_source_order() -> None:
    parsed_document = ParsedDocument(
        file_type="md",
        text="# Title\n\nFirst paragraph\nSecond paragraph\nThird paragraph",
        page_count=1,
        pages=[
            ParsedPage(
                page_number=1,
                text="# Title\n\nFirst paragraph\nSecond paragraph\nThird paragraph",
                char_count=len("# Title\n\nFirst paragraph\nSecond paragraph\nThird paragraph"),
            )
        ],
    )
    service = ChunkService(target_chunk_chars=6, min_chunk_chars=1, long_text_step=6)

    chunked = service.build_chunks(parsed_document)

    assert [chunk.chunk_index for chunk in chunked.chunks] == list(range(chunked.chunk_count))


def test_retrieval_service_handles_filler_words_and_title_bonus() -> None:
    parsed_document = ParsedDocument(
        file_type="md",
        text="# Project Goal\n\nThe first-phase goal is to support upload, summary, ask, and outline generation.\n# Background\n\nOther background information.",
        page_count=1,
        pages=[
            ParsedPage(
                page_number=1,
                text="# Project Goal\n\nThe first-phase goal is to support upload, summary, ask, and outline generation.\n# Background\n\nOther background information.",
                char_count=len("# Project Goal\n\nThe first-phase goal is to support upload, summary, ask, and outline generation.\n# Background\n\nOther background information."),
            )
        ],
    )
    chunked = ChunkService().build_chunks(parsed_document)
    retrieval = RetrievalService()

    selected = retrieval.retrieve("What should the first phase of the project do?", chunked)

    assert selected
    assert "first-phase goal" in selected[0].text.lower()


def test_retrieval_service_uses_head_chunk_for_metadata_name_questions() -> None:
    chunked = ChunkedDocument(
        file_type="md",
        page_count=1,
        chunk_count=1,
        chunks=[
            ParsedChunk(
                chunk_id="intro",
                chunk_index=0,
                page_numbers=[1],
                text="# 项目简介\n\n研答通是一款面向科研与智能办公场景的个人智能文档助理。",
                char_count=len("# 项目简介\n\n研答通是一款面向科研与智能办公场景的个人智能文档助理。"),
            )
        ],
    )
    retrieval = RetrievalService()

    result = retrieval.retrieve_with_confidence("这个产品的名字是什么？", chunked)

    assert result.confident is True
    assert [chunk.chunk_id for chunk in result.chunks] == ["intro"]


def test_retrieval_service_uses_head_chunks_for_overview_questions() -> None:
    chunked = ChunkedDocument(
        file_type="md",
        page_count=1,
        chunk_count=2,
        chunks=[
            ParsedChunk(
                chunk_id="intro",
                chunk_index=0,
                page_numbers=[1],
                text="# 论文标题\n\n本文研究中文空间语义理解评测，并比较多种大模型表现。",
                char_count=len("# 论文标题\n\n本文研究中文空间语义理解评测，并比较多种大模型表现。"),
            ),
            ParsedChunk(
                chunk_id="method",
                chunk_index=1,
                page_numbers=[1],
                text="方法部分介绍实验设置、数据集和评价指标。",
                char_count=len("方法部分介绍实验设置、数据集和评价指标。"),
            ),
        ],
    )
    retrieval = RetrievalService()

    result = retrieval.retrieve_with_confidence("这篇文章讲了什么", chunked)

    assert result.confident is True
    assert [chunk.chunk_id for chunk in result.chunks][:2] == ["intro", "method"]


def test_retrieval_service_treats_important_content_questions_as_overview() -> None:
    chunked = ChunkedDocument(
        file_type="md",
        page_count=1,
        chunk_count=2,
        chunks=[
            ParsedChunk(
                chunk_id="intro",
                chunk_index=0,
                page_numbers=[1],
                text="# 论文标题\n\n本文研究中文空间语义理解评测，并比较多种大模型表现。",
                char_count=len("# 论文标题\n\n本文研究中文空间语义理解评测，并比较多种大模型表现。"),
            ),
            ParsedChunk(
                chunk_id="method",
                chunk_index=1,
                page_numbers=[1],
                text="方法部分介绍实验设置、数据集和评价指标。",
                char_count=len("方法部分介绍实验设置、数据集和评价指标。"),
            ),
        ],
    )
    retrieval = RetrievalService()

    result = retrieval.retrieve_with_confidence("这篇文章最重要的内容是什么", chunked)

    assert result.confident is True
    assert [chunk.chunk_id for chunk in result.chunks][:2] == ["intro", "method"]


def test_retrieval_service_adds_neighbors_for_parameter_questions() -> None:
    retrieval = RetrievalService(top_k=1, max_context_chars=2000, min_score=0.0)
    chunked = ChunkedDocument(
        file_type="md",
        page_count=1,
        chunk_count=3,
        chunks=[
            ParsedChunk(
                chunk_id="before",
                chunk_index=0,
                page_numbers=[1],
                text="The section introduces model configuration.",
                char_count=len("The section introduces model configuration."),
            ),
            ParsedChunk(
                chunk_id="hit",
                chunk_index=1,
                page_numbers=[1],
                text="The base Transformer uses attention heads.",
                char_count=len("The base Transformer uses attention heads."),
            ),
            ParsedChunk(
                chunk_id="after",
                chunk_index=2,
                page_numbers=[1],
                text="In this work we employ h = 8 parallel attention layers, or heads.",
                char_count=len("In this work we employ h = 8 parallel attention layers, or heads."),
            ),
        ],
    )

    result = retrieval.retrieve_with_confidence(
        "How many attention heads does the base Transformer model use?", chunked
    )

    assert "hit" in [chunk.chunk_id for chunk in result.chunks]
    assert "after" in [chunk.chunk_id for chunk in result.chunks]


def test_retrieval_service_adds_head_chunks_for_contribution_questions() -> None:
    retrieval = RetrievalService(top_k=1, max_context_chars=2000, min_score=0.0)
    chunked = ChunkedDocument(
        file_type="md",
        page_count=2,
        chunk_count=3,
        chunks=[
            ParsedChunk(
                chunk_id="abstract",
                chunk_index=0,
                page_numbers=[1],
                text="Abstract: We propose the Transformer based entirely on attention.",
                char_count=len("Abstract: We propose the Transformer based entirely on attention."),
            ),
            ParsedChunk(
                chunk_id="intro",
                chunk_index=1,
                page_numbers=[2],
                text="The model replaces recurrence with self-attention for sequence transduction.",
                char_count=len("The model replaces recurrence with self-attention for sequence transduction."),
            ),
            ParsedChunk(
                chunk_id="tail-hit",
                chunk_index=2,
                page_numbers=[3],
                text="The contribution discussion includes efficient attention experiments.",
                char_count=len("The contribution discussion includes efficient attention experiments."),
            ),
        ],
    )

    result = retrieval.retrieve_with_confidence(
        "What are the main contributions of this paper?", chunked
    )

    assert "abstract" in [chunk.chunk_id for chunk in result.chunks]
    assert "intro" in [chunk.chunk_id for chunk in result.chunks]


def test_retrieval_normalize_query_preserves_english_tokens() -> None:
    retrieval = RetrievalService()

    normalized = retrieval._normalize_query("what is the architecture")

    assert normalized == "architecture"


def test_ask_prompt_includes_language_and_missing_info_contract() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        client = ModelClient(settings=settings)

        messages = client._build_messages(
            "ask",
            "Document says no rollback date is provided.",
            "What is the rollback date?",
            response_detail_level="balanced",
        )

        combined = "\n".join(message["content"] for message in messages)
        assert "回答语言必须跟随用户问题" in combined
        assert "不要把英文问题默认翻成中文回答" in combined
        assert "直接索要缺失字段的具体值" in combined
        assert "文档存在冲突但没有优先级规则" in combined
    finally:
        cleanup_workspace(workspace)


def test_ask_evidence_retry_keeps_conflict_and_language_contract() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        service = TaskService(
            file_service=FileService(settings=settings),
            model_client=ModelClient(settings=settings),
            log_service=LogService(settings=settings),
        )

        retry_input = service._build_ask_evidence_retry_input(
            "Who is the final owner for after-hours taxi approval?"
        )

        assert "回答语言必须跟随用户问题" in retry_input
        assert "不要把英文问题默认翻译成中文回答" in retry_input
        assert "存在互相冲突的信息且没有优先级规则" in retry_input
        assert "返回 refused=false" in retry_input
    finally:
        cleanup_workspace(workspace)


def test_model_client_retries_transient_urlerror(monkeypatch: pytest.MonkeyPatch) -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        settings.wuqiong_base_url = "https://example.com/api/v3"
        settings.wuqiong_api_key = "test-key"
        client = ModelClient(settings=settings)
        attempts = {"count": 0}

        class FakeResponse:
            headers = {"x-request-id": "req-abc"}

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def read(self):
                return b'{"id":"chatcmpl-123","choices":[{"message":{"content":"ok"}}],"usage":{"prompt_tokens":1,"completion_tokens":1,"total_tokens":2}}'

        def fake_urlopen(request, timeout):
            attempts["count"] += 1
            if attempts["count"] < 3:
                raise urllib.error.URLError("timed out")
            return FakeResponse()

        monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

        response, header_request_id = client._call_openai_compatible_api({"model": "x", "messages": []})

        assert response["choices"][0]["message"]["content"] == "ok"
        assert response["id"] == "chatcmpl-123"
        assert header_request_id == "req-abc"
        assert attempts["count"] == 3
    finally:
        cleanup_workspace(workspace)


class NeedMoreThenCiteModelClient(ModelClient):
    """First ask turn asks for more evidence + a followup query; second turn cites a
    chunk that can only be present if the agentic loop actually re-retrieved it."""

    def __init__(
        self,
        settings: Settings,
        *,
        followup_query: str,
        cite_chunk_id: str,
        cite_quote: str,
    ) -> None:
        super().__init__(settings=settings)
        self.ask_call_count = 0
        self._followup_query = followup_query
        self._cite_chunk_id = cite_chunk_id
        self._cite_quote = cite_quote
        self.second_call_document_text = ""

    def call_model(
        self,
        task_type: str,
        document_text: str,
        user_input: str | None = None,
        model_name_override: str | None = None,
        response_detail_level: ResponseDetailLevel = "balanced",
    ):
        base = super().call_model(
            task_type,
            document_text,
            user_input,
            model_name_override=model_name_override,
            response_detail_level=response_detail_level,
        )
        if task_type != "ask":
            return base
        self.ask_call_count += 1
        if self.ask_call_count == 1:
            payload = json.dumps(
                {
                    "refused": False,
                    "answer": "需要补充检索更多依据。",
                    "used_chunk_ids": [],
                    "evidence_quotes": [],
                    "need_more": True,
                    "followup_query": self._followup_query,
                },
                ensure_ascii=False,
            )
        else:
            self.second_call_document_text = document_text
            payload = json.dumps(
                {
                    "refused": False,
                    "answer": "已基于补充检索到的片段作答。",
                    "used_chunk_ids": [self._cite_chunk_id],
                    "evidence_quotes": [
                        {"chunk_id": self._cite_chunk_id, "quote": self._cite_quote}
                    ],
                },
                ensure_ascii=False,
            )
        return base.model_copy(update={"content": payload, "output_chars": len(payload)})


class FixedAskPlanner:
    def __init__(self, selected_chunks: list[ParsedChunk]) -> None:
        self.selected_chunks = selected_chunks

    def plan(self, **_kwargs) -> PlannedContext:
        context = "\n\n".join(
            f"【Chunk {chunk.chunk_id} | Pages {','.join(str(page) for page in chunk.page_numbers)}】\n{chunk.text}"
            for chunk in self.selected_chunks
        )
        return PlannedContext(
            strategy="retrieval_topk",
            document_text=context,
            selected_chunks=self.selected_chunks,
            retrieval_confident=True,
        )


class FollowupRetrieval(RetrievalService):
    def __init__(self, followup_chunks: list[ParsedChunk]) -> None:
        super().__init__()
        self._followup_chunks = followup_chunks

    def retrieve(self, query, chunked_document):  # type: ignore[override]
        return list(self._followup_chunks)


def test_agentic_ask_reretrieves_with_followup_query() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        upload = file_service.save_upload(
            "agentic.md",
            (
                "# Apple\n\nThe APPLEORCHARD section talks about red fruit.\n\n"
                "# Zebra\n\nThe ZEBRASTRIPES section talks about stripes."
            ).encode("utf-8"),
        )
        apple_chunk = ParsedChunk(
            chunk_id="apple-1",
            chunk_index=0,
            page_numbers=[1],
            text="The APPLEORCHARD section talks about red fruit and orchards.",
            char_count=59,
        )
        zebra_chunk = ParsedChunk(
            chunk_id="zebra-1",
            chunk_index=1,
            page_numbers=[1],
            text="The ZEBRASTRIPES section talks about black and white stripes on the savanna.",
            char_count=76,
        )
        model_client = NeedMoreThenCiteModelClient(
            settings,
            followup_query="ZEBRASTRIPES stripes savanna",
            cite_chunk_id="zebra-1",
            cite_quote="black and white stripes",
        )
        task_service = TaskService(
            file_service=file_service,
            model_client=model_client,
            log_service=LogService(settings=settings),
            retrieval_service=FollowupRetrieval([zebra_chunk]),
            context_planner=FixedAskPlanner([apple_chunk]),
        )

        result = task_service.run_task(
            task_type="ask",
            endpoint="/api/ask",
            file_id=upload.file_id,
            document_access_token=upload.access_token,
            user_input="Tell me about APPLEORCHARD",
        )

        # the loop made two model calls and re-retrieved a brand-new chunk in between
        assert model_client.ask_call_count == 2
        assert result.agent_iterations == 2
        assert result.query_rewrites == ["ZEBRASTRIPES stripes savanna"]
        # the re-retrieved chunk reached the model on the second turn
        assert "ZEBRASTRIPES" in model_client.second_call_document_text
        # and the final answer cites that newly retrieved chunk with validated evidence
        assert result.outcome == "answered"
        assert result.evidence_mode == "declared"
        assert "zebra-1" in result.used_chunk_ids
        assert any(citation.chunk_id == "zebra-1" for citation in result.citations)
        assert result.retrieved_chunk_count == 2
    finally:
        cleanup_workspace(workspace)


def test_validated_quotes_drop_fabricated_text() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        service = TaskService(
            file_service=FileService(settings=settings),
            model_client=ModelClient(settings=settings),
            log_service=LogService(settings=settings),
        )
        chunk = ParsedChunk(
            chunk_id="c1",
            chunk_index=0,
            page_numbers=[1],
            text="The transformer uses multi-head attention.",
            char_count=42,
        )
        selected_by_id = {"c1": chunk}

        kept = service._extract_validated_quotes(
            [{"chunk_id": "c1", "quote": "multi-head attention"}],
            ["c1"],
            selected_by_id,
        )
        assert [quote.quote for quote in kept] == ["multi-head attention"]

        dropped = service._extract_validated_quotes(
            [{"chunk_id": "c1", "quote": "quantum entanglement engine"}],
            ["c1"],
            selected_by_id,
        )
        assert dropped == []
    finally:
        cleanup_workspace(workspace)


def test_retrieval_skips_oversized_chunk_and_continues() -> None:
    retrieval = RetrievalService(top_k=2, max_context_chars=60, min_score=0.0)
    chunked = ChunkedDocument(
        file_type="md",
        page_count=1,
        chunk_count=3,
        chunks=[
            ParsedChunk(
                chunk_id="big",
                chunk_index=0,
                page_numbers=[1],
                text="method " * 80,
                char_count=len("method " * 80),
            ),
            ParsedChunk(
                chunk_id="small-1",
                chunk_index=1,
                page_numbers=[1],
                text="Method design note.",
                char_count=len("Method design note."),
            ),
            ParsedChunk(
                chunk_id="small-2",
                chunk_index=2,
                page_numbers=[1],
                text="Method advantages note.",
                char_count=len("Method advantages note."),
            ),
        ],
    )

    selected = retrieval.retrieve("method", chunked)

    assert [chunk.chunk_id for chunk in selected] == ["small-2", "small-1"]
