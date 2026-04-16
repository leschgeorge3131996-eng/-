from __future__ import annotations

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


def test_retrieval_normalize_query_preserves_english_tokens() -> None:
    retrieval = RetrievalService()

    normalized = retrieval._normalize_query("what is the architecture")

    assert normalized == "architecture"


def test_model_client_retries_transient_urlerror(monkeypatch: pytest.MonkeyPatch) -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        settings.wuqiong_base_url = "https://example.com/api/v3"
        settings.wuqiong_api_key = "test-key"
        client = ModelClient(settings=settings)
        attempts = {"count": 0}

        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def read(self):
                return b'{"choices":[{"message":{"content":"ok"}}],"usage":{"prompt_tokens":1,"completion_tokens":1,"total_tokens":2}}'

        def fake_urlopen(request, timeout):
            attempts["count"] += 1
            if attempts["count"] < 3:
                raise urllib.error.URLError("timed out")
            return FakeResponse()

        monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

        response = client._call_openai_compatible_api({"model": "x", "messages": []})

        assert response["choices"][0]["message"]["content"] == "ok"
        assert attempts["count"] == 3
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

