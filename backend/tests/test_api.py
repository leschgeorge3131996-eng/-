from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app.api import routes
from backend.app.core.config import Settings
from backend.app.main import app
from backend.app.services.cache_service import CacheService
from backend.app.services.file_service import FileService
from backend.app.services.log_service import LogService
from backend.app.services.model_client import ModelClient
from backend.app.services.task_service import TaskService


def make_workspace() -> Path:
    root = Path.cwd() / ".test_tmp" / uuid4().hex
    root.mkdir(parents=True, exist_ok=True)
    return root


def cleanup_workspace(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)


def build_settings(tmp_root: Path, *, max_document_chars: int = 10000) -> Settings:
    data_dir = tmp_root / "data"
    settings = Settings(
        project_root=tmp_root,
        app_name="test-app",
        app_env="test",
        api_prefix="/api",
        cors_origins=["http://localhost:5173"],
        log_level="INFO",
        max_upload_mb=5,
        max_document_chars=max_document_chars,
        request_timeout_seconds=30,
        data_dir=data_dir,
        uploads_dir=data_dir / "uploads",
        parsed_dir=data_dir / "parsed",
        logs_dir=data_dir / "logs",
        cache_dir=data_dir / "cache",
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


def build_client(tmp_root: Path, *, max_document_chars: int = 10000) -> TestClient:
    settings = build_settings(tmp_root, max_document_chars=max_document_chars)
    file_service = FileService(settings=settings)
    log_service = LogService(settings=settings)
    model_client = ModelClient(settings=settings)
    task_service = TaskService(
        file_service=file_service,
        model_client=model_client,
        log_service=log_service,
        cache_service=CacheService(settings=settings),
    )

    routes.settings = settings
    routes.file_service = file_service
    routes.log_service = log_service
    routes.task_service = task_service

    return TestClient(app)


def test_upload_endpoint_returns_fingerprint() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)
        response = client.post(
            "/api/upload",
            files={"file": ("demo.md", "# 标题\n\n内容".encode("utf-8"), "text/markdown")},
        )

        assert response.status_code == 200
        payload = response.json()["data"]["metadata"]
        assert payload["parse_status"] == "parsed"
        assert payload["document_fingerprint"]
    finally:
        cleanup_workspace(workspace)


def test_summary_endpoint_returns_truncation_fields() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace, max_document_chars=20)
        upload_response = client.post(
            "/api/upload",
            files={"file": ("demo.txt", "这是一个很长的测试文档内容，用来验证截断提示是否明确。".encode("utf-8"), "text/plain")},
        )
        file_id = upload_response.json()["data"]["metadata"]["file_id"]

        response = client.post(
            "/api/summary",
            json={"file_id": file_id, "instruction": "请总结"},
        )

        assert response.status_code == 200
        payload = response.json()["data"]
        assert payload["context_truncated"] is True
        assert payload["source_document_chars"] > payload["used_document_chars"]
        assert payload["truncation_message"]
        assert payload["document_fingerprint"]
    finally:
        cleanup_workspace(workspace)


def test_logs_summary_endpoint_returns_aggregates() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)
        upload_response = client.post(
            "/api/upload",
            files={"file": ("demo.md", "# 标题\n\n用于日志测试".encode("utf-8"), "text/markdown")},
        )
        file_id = upload_response.json()["data"]["metadata"]["file_id"]

        client.post("/api/summary", json={"file_id": file_id, "instruction": "请总结"})
        client.post("/api/ask", json={"file_id": file_id, "question": "这是什么文档？"})

        response = client.get("/api/logs/summary")

        assert response.status_code == 200
        payload = response.json()["data"]
        assert payload["total_requests"] >= 2
        assert payload["success_count"] >= 2
        assert "summary" in payload["by_task"]
        assert "ask" in payload["by_task"]
    finally:
        cleanup_workspace(workspace)

