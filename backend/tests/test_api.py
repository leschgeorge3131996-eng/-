from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app.api import routes
from backend.app.core.config import Settings
from backend.app.main import app
from backend.app.services.auth_service import AuthService
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
    alpha_invite_codes: list[str] | None = None,
    demo_mode: bool = False,
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
        document_retention_hours=72,
        session_retention_hours=168,
        session_cookie_name="yandatong_session",
        session_cookie_secure=False,
        session_cookie_samesite="lax",
        alpha_invite_codes=alpha_invite_codes or ["invite-123"],
        demo_mode=demo_mode,
        data_dir=data_dir,
        uploads_dir=data_dir / "uploads",
        parsed_dir=data_dir / "parsed",
        sessions_dir=data_dir / "sessions",
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
    alpha_invite_codes: list[str] | None = None,
    demo_mode: bool = False,
) -> TestClient:
    settings = build_settings(
        tmp_root,
        max_document_chars=max_document_chars,
        model_lite=model_lite,
        model_pro=model_pro,
        route_upgrade_chars=route_upgrade_chars,
        alpha_invite_codes=alpha_invite_codes,
        demo_mode=demo_mode,
    )
    auth_service = AuthService(settings=settings)
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
    routes.auth_service = auth_service
    routes.file_service = file_service
    routes.log_service = log_service
    routes.task_service = task_service

    return TestClient(app)


def login(
    client: TestClient,
    *,
    invite_code: str = "invite-123",
    display_name: str = "tester",
) -> dict[str, str]:
    response = client.post(
        "/api/auth/login",
        json={"invite_code": invite_code, "display_name": display_name},
    )
    assert response.status_code == 200
    assert client.cookies.get(routes.settings.session_cookie_name)
    return {}


def upload_document(
    client: TestClient,
    filename: str,
    content: bytes,
    content_type: str,
    *,
    headers: dict[str, str],
) -> dict:
    response = client.post(
        "/api/upload",
        files={"file": (filename, content, content_type)},
        headers=headers,
    )
    assert response.status_code == 200
    return response.json()["data"]["metadata"]


def test_login_sets_cookie_and_returns_current_session() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)

        login_response = client.post(
            "/api/auth/login",
            json={"invite_code": "invite-123", "display_name": "alpha-user"},
        )

        assert login_response.status_code == 200
        payload = login_response.json()["data"]
        assert payload["session"]["label"] == "alpha-user"
        assert "session_token" not in payload
        cookie_header = login_response.headers.get("set-cookie", "")
        assert f"{routes.settings.session_cookie_name}=" in cookie_header
        assert "HttpOnly" in cookie_header

        session_response = client.get("/api/auth/session")

        assert session_response.status_code == 200
        assert session_response.json()["data"]["session"]["label"] == "alpha-user"
    finally:
        cleanup_workspace(workspace)


def test_demo_session_disabled_by_default() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)
        response = client.post("/api/auth/demo-session")
        assert response.status_code == 401
        assert "演示" in response.json()["error"]["message"]
    finally:
        cleanup_workspace(workspace)


def test_demo_session_creates_cookie_backed_session_when_enabled() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace, demo_mode=True)

        response = client.post("/api/auth/demo-session")

        assert response.status_code == 200
        payload = response.json()["data"]
        assert payload["session"]["label"].startswith("demo-")
        cookie_header = response.headers.get("set-cookie", "")
        assert f"{routes.settings.session_cookie_name}=" in cookie_header
        assert "HttpOnly" in cookie_header

        session_response = client.get("/api/auth/session")
        assert session_response.status_code == 200

        health_response = client.get("/api/health")
        assert health_response.json()["data"]["demo_mode"] is True
    finally:
        cleanup_workspace(workspace)


def test_upload_requires_authenticated_session() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)

        response = client.post(
            "/api/upload",
            files={"file": ("demo.md", b"# title\n\nbody", "text/markdown")},
        )

        assert response.status_code == 401
        assert response.json()["error"]["code"] == "UNAUTHORIZED"
    finally:
        cleanup_workspace(workspace)


def test_header_only_session_token_is_rejected() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)
        login(client)
        cookie_token = client.cookies.get(routes.settings.session_cookie_name)
        assert cookie_token

        anonymous_client = TestClient(app)
        response = anonymous_client.get(
            "/api/auth/session",
            headers={"X-Session-Token": cookie_token},
        )

        assert response.status_code == 401
        assert response.json()["error"]["code"] == "UNAUTHORIZED"
    finally:
        cleanup_workspace(workspace)


def test_logout_revokes_cookie_backed_session() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)
        login(client)

        logout_response = client.post("/api/auth/logout")
        session_response = client.get("/api/auth/session")

        assert logout_response.status_code == 200
        assert logout_response.json()["data"]["logged_out"] is True
        cleared_cookie = logout_response.headers.get("set-cookie", "")
        assert f"{routes.settings.session_cookie_name}=" in cleared_cookie
        assert "max-age=0" in cleared_cookie.lower()
        assert session_response.status_code == 401
    finally:
        cleanup_workspace(workspace)


def test_upload_endpoint_returns_fingerprint_and_access_token() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)
        headers = login(client)
        metadata = upload_document(
            client,
            "demo.md",
            "# Title\n\nBody".encode("utf-8"),
            "text/markdown",
            headers=headers,
        )

        assert metadata["parse_status"] == "parsed"
        assert metadata["document_fingerprint"]
        assert metadata["access_token"]
        assert metadata["expires_at"]
        assert metadata["page_count"] == 1
        assert metadata["chunk_count"] >= 1
    finally:
        cleanup_workspace(workspace)


def test_summary_endpoint_returns_truncation_fields() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace, max_document_chars=20)
        headers = login(client)
        metadata = upload_document(
            client,
            "demo.txt",
            ("This is a deliberately long document body used to exercise truncation.").encode("utf-8"),
            "text/plain",
            headers=headers,
        )

        response = client.post(
            "/api/summary",
            json={
                "file_id": metadata["file_id"],
                "document_access_token": metadata["access_token"],
                "instruction": "Summarize the document",
                "response_detail_level": "detailed",
            },
            headers=headers,
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
        headers = login(client)
        metadata = upload_document(
            client,
            "demo.md",
            "# Title\n\nUsed for log summary".encode("utf-8"),
            "text/markdown",
            headers=headers,
        )

        client.post(
            "/api/summary",
            json={
                "file_id": metadata["file_id"],
                "document_access_token": metadata["access_token"],
                "instruction": "Summarize",
            },
            headers=headers,
        )
        client.post(
            "/api/ask",
            json={
                "file_id": metadata["file_id"],
                "document_access_token": metadata["access_token"],
                "question": "What is this document?",
            },
            headers=headers,
        )

        response = client.get("/api/logs/summary", headers=headers)

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
        headers = login(client)
        metadata = upload_document(
            client,
            "demo.md",
            "# Background\n\nSome setup.\n\n# Goal\n\nThe first phase supports document upload.".encode("utf-8"),
            "text/markdown",
            headers=headers,
        )

        response = client.post(
            "/api/ask",
            json={
                "file_id": metadata["file_id"],
                "document_access_token": metadata["access_token"],
                "question": "What does the first phase support?",
            },
            headers=headers,
        )

        assert response.status_code == 200
        payload = response.json()["data"]
        assert payload["outcome"] == "answered"
        assert payload["retrieval_applied"] is True
        assert payload["retrieved_chunk_count"] >= 1
        assert payload["retrieved_pages"] == [1]
        assert len(payload["citations"]) >= 1
        assert payload["candidate_chunks"] == []
        assert payload["source_chunks"] == []
    finally:
        cleanup_workspace(workspace)


def test_ask_endpoint_returns_no_citations_when_not_retrieved() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)
        headers = login(client)
        metadata = upload_document(
            client,
            "demo.md",
            "# Document\n\nThis discusses only background and scope.".encode("utf-8"),
            "text/markdown",
            headers=headers,
        )

        response = client.post(
            "/api/ask",
            json={
                "file_id": metadata["file_id"],
                "document_access_token": metadata["access_token"],
                "question": "A completely unrelated astronomy question",
            },
            headers=headers,
        )

        assert response.status_code == 200
        payload = response.json()["data"]
        assert payload["outcome"] == "refused"
        assert payload["retrieval_status"] == "no_match"
        assert payload["retrieval_message"]
        assert payload["retrieval_applied"] is False
        assert payload["retrieved_chunk_count"] == 0
        assert payload["citations"] == []
        assert payload["candidate_chunks"] == []
        assert payload["source_chunks"] == []
    finally:
        cleanup_workspace(workspace)


def test_summary_endpoint_returns_route_fields_when_tiered() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace, model_lite="lite-model", model_pro="pro-model")
        headers = login(client)
        metadata = upload_document(
            client,
            "demo.md",
            "# Title\n\nBody".encode("utf-8"),
            "text/markdown",
            headers=headers,
        )

        response = client.post(
            "/api/summary",
            json={
                "file_id": metadata["file_id"],
                "document_access_token": metadata["access_token"],
                "instruction": "Summarize",
            },
            headers=headers,
        )

        assert response.status_code == 200
        payload = response.json()["data"]
        assert payload["route_tier"] == "lite"
        assert payload["route_model"] == "lite-model"
    finally:
        cleanup_workspace(workspace)


def test_file_content_endpoint_requires_session_and_access_token() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)
        headers = login(client)
        anonymous_client = TestClient(app)
        metadata = upload_document(
            client,
            "demo.md",
            "# title\n\nbody".encode("utf-8"),
            "text/markdown",
            headers=headers,
        )

        unauthorized_response = anonymous_client.get(
            f"/api/files/{metadata['file_id']}/content"
        )
        forbidden_response = client.get(
            f"/api/files/{metadata['file_id']}/content",
            headers=headers,
        )
        fetch_response = client.get(
            f"/api/files/{metadata['file_id']}/content?access_token={metadata['access_token']}",
            headers=headers,
        )

        assert unauthorized_response.status_code == 401
        assert forbidden_response.status_code == 403
        assert fetch_response.status_code == 200
        assert fetch_response.content == b"# title\n\nbody"
        assert "inline" in fetch_response.headers.get("content-disposition", "")
    finally:
        cleanup_workspace(workspace)


def test_file_metadata_endpoint_returns_upload_metadata() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)
        headers = login(client)
        metadata = upload_document(
            client,
            "demo.md",
            "# title\n\nbody".encode("utf-8"),
            "text/markdown",
            headers=headers,
        )

        fetch_response = client.get(
            f"/api/files/{metadata['file_id']}/metadata?access_token={metadata['access_token']}",
            headers=headers,
        )

        assert fetch_response.status_code == 200
        payload = fetch_response.json()["data"]["metadata"]
        assert payload["file_id"] == metadata["file_id"]
        assert payload["original_name"] == "demo.md"
        assert payload["file_type"] == "md"
        assert payload["page_count"] == 1
        assert payload["access_token"] == metadata["access_token"]
    finally:
        cleanup_workspace(workspace)


def test_file_page_endpoint_returns_page_text() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)
        headers = login(client)
        metadata = upload_document(
            client,
            "demo.md",
            "# title\n\nbody".encode("utf-8"),
            "text/markdown",
            headers=headers,
        )

        fetch_response = client.get(
            f"/api/files/{metadata['file_id']}/pages/1?access_token={metadata['access_token']}",
            headers=headers,
        )

        assert fetch_response.status_code == 200
        payload = fetch_response.json()["data"]
        assert payload["page_number"] == 1
        assert payload["text"] == "# title\n\nbody"
        assert payload["char_count"] > 0
    finally:
        cleanup_workspace(workspace)


def test_delete_file_endpoint_removes_document_and_blocks_future_access() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)
        headers = login(client)
        metadata = upload_document(
            client,
            "demo.md",
            "# title\n\nbody".encode("utf-8"),
            "text/markdown",
            headers=headers,
        )

        delete_response = client.delete(
            f"/api/files/{metadata['file_id']}?access_token={metadata['access_token']}",
            headers=headers,
        )
        metadata_response = client.get(
            f"/api/files/{metadata['file_id']}/metadata?access_token={metadata['access_token']}",
            headers=headers,
        )

        assert delete_response.status_code == 200
        assert delete_response.json()["data"]["deleted"] is True
        assert metadata_response.status_code == 404
    finally:
        cleanup_workspace(workspace)


def test_task_endpoints_require_document_access_token() -> None:
    workspace = make_workspace()
    try:
        client = build_client(workspace)
        headers = login(client)
        metadata = upload_document(
            client,
            "demo.md",
            "# title\n\nbody".encode("utf-8"),
            "text/markdown",
            headers=headers,
        )

        response = client.post(
            "/api/summary",
            json={"file_id": metadata["file_id"], "instruction": "Summarize"},
            headers=headers,
        )

        assert response.status_code == 403
        assert response.json()["error"]["code"] == "FORBIDDEN"
    finally:
        cleanup_workspace(workspace)


def test_document_access_is_isolated_between_sessions() -> None:
    workspace = make_workspace()
    try:
        owner_client = build_client(workspace)
        other_client = TestClient(app)
        owner_headers = login(owner_client, display_name="owner")
        other_headers = login(other_client, display_name="other")
        metadata = upload_document(
            owner_client,
            "demo.md",
            "# title\n\nbody".encode("utf-8"),
            "text/markdown",
            headers=owner_headers,
        )

        response = other_client.get(
            f"/api/files/{metadata['file_id']}/metadata?access_token={metadata['access_token']}",
            headers=other_headers,
        )

        assert response.status_code == 403
        assert response.json()["error"]["code"] == "FORBIDDEN"
    finally:
        cleanup_workspace(workspace)
