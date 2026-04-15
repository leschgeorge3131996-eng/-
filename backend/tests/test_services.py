from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

import pytest

from backend.app.core.exceptions import ParseError

from backend.app.core.config import Settings
from backend.app.schemas.log import CallLogEntry
from backend.app.services.file_service import FileService
from backend.app.services.log_service import LogService
from backend.app.services.model_client import ModelClient
from backend.app.services.task_service import TaskService
from backend.app.services.document_parser import DocumentParser


def make_workspace() -> Path:
    root = Path.cwd() / ".test_tmp" / uuid4().hex
    root.mkdir(parents=True, exist_ok=True)
    return root


def cleanup_workspace(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)


def build_settings(tmp_root: Path) -> Settings:
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
        data_dir=data_dir,
        uploads_dir=uploads_dir,
        parsed_dir=parsed_dir,
        logs_dir=logs_dir,
        cache_dir=cache_dir,
        model_provider="mock",
        use_mock_model=True,
        wuqiong_base_url="",
        wuqiong_api_key="",
        model_qa="mock-qa",
        model_summary="mock-summary",
        model_outline="mock-outline",
    )
    settings.ensure_directories()
    return settings


def test_save_upload_and_load_text() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        service = FileService(settings=settings)

        result = service.save_upload("demo.txt", "第一段\n第二段".encode("utf-8"))
        text = service.get_document_text(result.file_id)

        assert result.parse_status == "parsed"
        assert result.text_chars > 0
        assert "第一段" in text
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
            "# 标题\n\n这是一个测试文档。\n\n包含研究背景与方法。".encode("utf-8"),
        )
        result = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            user_input="请突出创新点",
        )
        logs = log_service.list_logs(limit=10)

        assert result.task_type == "summary"
        assert result.request_id
        assert logs
        assert logs[0]["success"] is True
        assert logs[0]["task_type"] == "summary"
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
    ):
        self.call_count += 1
        return super().call_model(task_type, document_text, user_input)


def test_parse_error_is_normalized() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        service = FileService(settings=settings, parser=BrokenPdfParser())

        with pytest.raises(ParseError):
            service.save_upload("bad.pdf", b"%PDF-1.4 fake")
    finally:
        cleanup_workspace(workspace)


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
        upload = file_service.save_upload("demo.txt", "一段测试内容".encode("utf-8"))

        result = task_service.run_task(
            task_type="ask",
            endpoint="/api/ask",
            file_id=upload.file_id,
            user_input="这段内容说了什么？",
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
                    '{"request_id":"1","timestamp":"2026-04-15T01:00:00+00:00","endpoint":"/api/summary","task_type":"summary","model_name":"m1","success":true,"latency_ms":100,"prompt_chars":10,"output_chars":20,"token_total":30,"cache_hit":false}',
                    '{"request_id":"2","timestamp":"2026-04-15T01:01:00+00:00","endpoint":"/api/ask","task_type":"ask","model_name":"m1","success":false,"latency_ms":400,"prompt_chars":10,"output_chars":0,"token_total":0,"cache_hit":false,"error_type":"MODEL_SERVICE_ERROR"}',
                    '{"request_id":"3","timestamp":"2026-04-15T01:02:00+00:00","endpoint":"/api/summary","task_type":"summary","model_name":"m2","success":true,"latency_ms":200,"prompt_chars":10,"output_chars":20,"token_total":40,"cache_hit":true}',
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
        assert summary["token_total_sum"] == 70
        assert summary["by_task"]["summary"] == 2
        assert summary["by_task"]["ask"] == 1
        assert summary["by_model"]["m1"] == 2
        assert summary["by_model"]["m2"] == 1
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
        upload = file_service.save_upload("demo.txt", "缓存测试内容".encode("utf-8"))

        first = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            user_input="请总结",
        )
        second = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            user_input="请总结",
        )

        assert first.cache_hit is False
        assert second.cache_hit is True
        assert model_client.call_count == 1
        assert first.result == second.result
    finally:
        cleanup_workspace(workspace)
