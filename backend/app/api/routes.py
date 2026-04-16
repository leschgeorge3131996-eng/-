from __future__ import annotations

from fastapi import APIRouter, Depends, File, Query, Request, Response, UploadFile
from fastapi.responses import FileResponse

from ..core.config import get_settings
from ..core.exceptions import UnauthorizedError
from ..schemas.auth import LoginRequest, SessionData
from ..schemas.common import ApiResponse, success_response
from ..schemas.task import AskRequest, TaskRequest
from ..services.auth_service import AuthService
from ..services.file_service import FileService
from ..services.log_service import LogService
from ..services.task_service import TaskService

router = APIRouter()
settings = get_settings()
auth_service = AuthService(settings=settings)
file_service = FileService(settings=settings)
log_service = LogService(settings=settings)
task_service = TaskService(file_service=file_service, log_service=log_service)


def resolve_session_token(
    request: Request,
) -> str | None:
    return request.cookies.get(settings.session_cookie_name)


def set_session_cookie(response: Response, session_token: str) -> None:
    response.set_cookie(
        key=settings.session_cookie_name,
        value=session_token,
        max_age=settings.session_retention_hours * 3600,
        httponly=True,
        secure=settings.session_cookie_secure,
        samesite=settings.session_cookie_samesite,
        path="/",
    )


def clear_session_cookie(response: Response) -> None:
    response.delete_cookie(
        key=settings.session_cookie_name,
        httponly=True,
        secure=settings.session_cookie_secure,
        samesite=settings.session_cookie_samesite,
        path="/",
    )


def require_session(
    session_token: str | None = Depends(resolve_session_token),
) -> SessionData:
    if not session_token:
        raise UnauthorizedError("请先通过邀请码登录后再继续。")
    return auth_service.get_session(session_token)


@router.get("/health", response_model=ApiResponse)
def health_check() -> ApiResponse:
    return success_response(
        {
            "status": "ok",
            "app_name": settings.app_name,
            "environment": settings.app_env,
            "model_provider": settings.model_provider,
            "use_mock_model": settings.use_mock_model,
            "demo_mode": settings.demo_mode,
        }
    )


@router.post("/auth/login", response_model=ApiResponse)
def login(payload: LoginRequest, response: Response) -> ApiResponse:
    session = auth_service.create_session(
        payload.invite_code,
        display_name=payload.display_name,
    )
    set_session_cookie(response, session.session_token)
    return success_response({"session": session.session.model_dump()})


@router.post("/auth/demo-session", response_model=ApiResponse)
def create_demo_session(response: Response) -> ApiResponse:
    session = auth_service.create_demo_session()
    set_session_cookie(response, session.session_token)
    return success_response({"session": session.session.model_dump()})


@router.get("/auth/session", response_model=ApiResponse)
def get_current_session(session: SessionData = Depends(require_session)) -> ApiResponse:
    return success_response({"session": session.model_dump()})


@router.post("/auth/logout", response_model=ApiResponse)
def logout(
    response: Response,
    session_token: str | None = Depends(resolve_session_token),
    _: SessionData = Depends(require_session),
) -> ApiResponse:
    if not session_token:
        raise UnauthorizedError("当前试用会话不存在或已失效，请重新登录。")
    auth_service.revoke_session(session_token)
    clear_session_cookie(response)
    return success_response({"logged_out": True})


@router.post("/upload", response_model=ApiResponse)
async def upload_document(
    file: UploadFile = File(...),
    session: SessionData = Depends(require_session),
) -> ApiResponse:
    content = await file.read()
    result = file_service.save_upload(
        file.filename or "",
        content,
        owner_session_id=session.session_id,
    )
    return success_response({"metadata": result.model_dump()})


@router.get("/files/{file_id}/content")
def get_uploaded_file_content(
    file_id: str,
    access_token: str | None = Query(default=None),
    session: SessionData = Depends(require_session),
) -> FileResponse:
    metadata = file_service.get_document_metadata(
        file_id,
        access_token=access_token,
        session_id=session.session_id,
    )
    file_path = file_service.get_upload_path(
        file_id,
        access_token=access_token,
        session_id=session.session_id,
    )
    media_type = file_service.get_upload_media_type(
        file_id,
        access_token=access_token,
        session_id=session.session_id,
    )
    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=metadata.original_name,
        content_disposition_type="inline",
    )


@router.get("/files/{file_id}/metadata", response_model=ApiResponse)
def get_uploaded_file_metadata(
    file_id: str,
    access_token: str | None = Query(default=None),
    session: SessionData = Depends(require_session),
) -> ApiResponse:
    metadata = file_service.get_document_metadata(
        file_id,
        access_token=access_token,
        session_id=session.session_id,
    )
    return success_response(
        {
            "metadata": {
                "file_id": metadata.file_id,
                "original_name": metadata.original_name,
                "access_token": metadata.access_token,
                "file_type": metadata.file_type,
                "size_bytes": metadata.size_bytes,
                "text_chars": metadata.text_chars,
                "page_count": metadata.page_count,
                "chunk_count": metadata.chunk_count,
                "document_fingerprint": metadata.document_fingerprint,
                "expires_at": metadata.expires_at,
                "parse_status": metadata.parse_status,
            }
        }
    )


@router.get("/files/{file_id}/pages/{page_number}", response_model=ApiResponse)
def get_uploaded_file_page(
    file_id: str,
    page_number: int,
    access_token: str | None = Query(default=None),
    session: SessionData = Depends(require_session),
) -> ApiResponse:
    page = file_service.get_document_page(
        file_id,
        page_number,
        access_token=access_token,
        session_id=session.session_id,
    )
    return success_response(
        {
            "page_number": page.page_number,
            "char_count": page.char_count,
            "text": page.text,
        }
    )


@router.delete("/files/{file_id}", response_model=ApiResponse)
def delete_uploaded_file(
    file_id: str,
    access_token: str | None = Query(default=None),
    session: SessionData = Depends(require_session),
) -> ApiResponse:
    metadata = file_service.delete_document(
        file_id,
        access_token=access_token,
        session_id=session.session_id,
    )
    return success_response(
        {
            "deleted": True,
            "file_id": metadata.file_id,
            "original_name": metadata.original_name,
        }
    )


@router.post("/ask", response_model=ApiResponse)
def ask_document(
    payload: AskRequest,
    session: SessionData = Depends(require_session),
) -> ApiResponse:
    result = task_service.run_task(
        task_type="ask",
        endpoint="/api/ask",
        file_id=payload.file_id,
        session_id=session.session_id,
        document_access_token=payload.document_access_token,
        user_input=payload.question,
        response_detail_level=payload.response_detail_level,
    )
    return success_response(result.model_dump(), request_id=result.request_id)


@router.post("/summary", response_model=ApiResponse)
def summarize_document(
    payload: TaskRequest,
    session: SessionData = Depends(require_session),
) -> ApiResponse:
    result = task_service.run_task(
        task_type="summary",
        endpoint="/api/summary",
        file_id=payload.file_id,
        session_id=session.session_id,
        document_access_token=payload.document_access_token,
        user_input=payload.instruction,
        response_detail_level=payload.response_detail_level,
    )
    return success_response(result.model_dump(), request_id=result.request_id)


@router.post("/outline", response_model=ApiResponse)
def outline_document(
    payload: TaskRequest,
    session: SessionData = Depends(require_session),
) -> ApiResponse:
    result = task_service.run_task(
        task_type="outline",
        endpoint="/api/outline",
        file_id=payload.file_id,
        session_id=session.session_id,
        document_access_token=payload.document_access_token,
        user_input=payload.instruction,
        response_detail_level=payload.response_detail_level,
    )
    return success_response(result.model_dump(), request_id=result.request_id)


@router.get("/logs", response_model=ApiResponse)
def recent_logs(
    limit: int = Query(default=20, ge=1, le=100),
    _: SessionData = Depends(require_session),
) -> ApiResponse:
    return success_response({"items": log_service.list_logs(limit=limit)})


@router.get("/logs/summary", response_model=ApiResponse)
def logs_summary(
    limit: int | None = Query(default=None, ge=1, le=1000),
    _: SessionData = Depends(require_session),
) -> ApiResponse:
    return success_response(log_service.summarize_logs(limit=limit))
