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


def build_settings(
    tmp_root: Path,
    *,
    max_document_chars: int = 10000,
    model_lite: str = "",
    model_pro: str = "",
    route_upgrade_chars: int = 12000,
) -> Settings:
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
        model_lite=model_lite,
        model_pro=model_pro,
        model_qa="mock-qa",
        model_summary="mock-summary",
        model_outline="mock-outline",
        route_upgrade_chars=route_upgrade_chars,
    )
    settings.ensure_directories()
    return settings


def build_client(
    tmp_root: Path,
    *,
    max_document_chars: int = 10000,
    model_lite: str = "",
    model_pro: str = "",
    route_upgrade_chars: int = 12000,
) -> TestClient:
    settings = build_settings(
        tmp_root,
        max_document_chars=max_document_chars,
        model_lite=model_lite,
        model_pro=model_pro,
        route_upgrade_chars=route_upgrade_chars,
    )
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
        assert payload["page_count"] == 1
        assert payload["chunk_count"] >= 1
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
            json={"file_id": file_id, "instruction": "请总结", "response_detail_level": "detailed"},
        )

        assert response.status_code == 200
        payload = response.json()["data"]
        assert payload["context_truncated"] is True
        assert payload["source_document_chars"] > payload["used_document_chars"]
        assert payload["truncation_message"]
        assert payload["document_fingerprint"]
        assert payload["response_detail_level"] == "detailed"
        assert payload["citations"] == []
        assert len(payload["source_chunks"]) >= 1
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


def test_ask_endpoint_returns_retrieval_fields() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)
        upload_response = client.post(
            "/api/upload",
            files={"file": ("demo.md", "# 背景\n\n一些背景。\n\n# 目标\n\n第一阶段目标是支持上传文档。".encode("utf-8"), "text/markdown")},
        )
        file_id = upload_response.json()["data"]["metadata"]["file_id"]

        response = client.post(
            "/api/ask",
            json={"file_id": file_id, "question": "第一阶段目标是什么？"},
        )

        assert response.status_code == 200
        payload = response.json()["data"]
        assert payload["outcome"] == "answered"
        assert payload["retrieval_applied"] is True
        assert payload["retrieved_chunk_count"] >= 1
        assert payload["retrieved_pages"] == [1]
        assert len(payload["citations"]) >= 1
        assert payload["citations"][0]["page_numbers"] == [1]
        assert payload["source_chunks"] == []
    finally:
        cleanup_workspace(workspace)


def test_ask_endpoint_returns_no_citations_when_not_retrieved() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)
        upload_response = client.post(
            "/api/upload",
            files={"file": ("demo.md", "# 文档\n\n这里讨论项目背景和目标。".encode("utf-8"), "text/markdown")},
        )
        file_id = upload_response.json()["data"]["metadata"]["file_id"]

        response = client.post(
            "/api/ask",
            json={"file_id": file_id, "question": "完全不相关的天文问题"},
        )

        assert response.status_code == 200
        payload = response.json()["data"]
        assert payload["outcome"] == "refused"
        assert payload["retrieval_status"] == "no_match"
        assert payload["retrieval_message"]
        assert payload["retrieval_applied"] is False
        assert payload["retrieved_chunk_count"] == 0
        assert payload["citations"] == []
        assert payload["source_chunks"] == []
    finally:
        cleanup_workspace(workspace)


def test_summary_endpoint_returns_route_fields_when_tiered() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace, model_lite="lite-model", model_pro="pro-model")
        upload_response = client.post(
            "/api/upload",
            files={"file": ("demo.md", "# 标题\n\n内容".encode("utf-8"), "text/markdown")},
        )
        file_id = upload_response.json()["data"]["metadata"]["file_id"]

        response = client.post(
            "/api/summary",
            json={"file_id": file_id, "instruction": "请总结"},
        )

        assert response.status_code == 200
        payload = response.json()["data"]
        assert payload["route_tier"] == "lite"
        assert payload["route_model"] == "lite-model"
    finally:
        cleanup_workspace(workspace)


def test_file_content_endpoint_returns_inline_uploaded_file() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)
        response = client.post(
            "/api/upload",
            files={"file": ("demo.md", "# title\n\nbody".encode("utf-8"), "text/markdown")},
        )
        file_id = response.json()["data"]["metadata"]["file_id"]

        fetch_response = client.get(f"/api/files/{file_id}/content")

        assert fetch_response.status_code == 200
        assert fetch_response.content == b"# title\n\nbody"
        assert "inline" in fetch_response.headers.get("content-disposition", "")
    finally:
        cleanup_workspace(workspace)


def test_file_metadata_endpoint_returns_upload_metadata() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)
        response = client.post(
            "/api/upload",
            files={"file": ("demo.md", "# title\n\nbody".encode("utf-8"), "text/markdown")},
        )
        file_id = response.json()["data"]["metadata"]["file_id"]

        fetch_response = client.get(f"/api/files/{file_id}/metadata")

        assert fetch_response.status_code == 200
        payload = fetch_response.json()["data"]["metadata"]
        assert payload["file_id"] == file_id
        assert payload["original_name"] == "demo.md"
        assert payload["file_type"] == "md"
        assert payload["page_count"] == 1
    finally:
        cleanup_workspace(workspace)


def test_file_page_endpoint_returns_page_text() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)
        response = client.post(
            "/api/upload",
            files={"file": ("demo.md", "# title\n\nbody".encode("utf-8"), "text/markdown")},
        )
        file_id = response.json()["data"]["metadata"]["file_id"]

        fetch_response = client.get(f"/api/files/{file_id}/pages/1")

        assert fetch_response.status_code == 200
        payload = fetch_response.json()["data"]
        assert payload["page_number"] == 1
        assert payload["text"] == "# title\n\nbody"
        assert payload["char_count"] > 0
    finally:
        cleanup_workspace(workspace)
