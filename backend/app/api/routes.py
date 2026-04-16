from __future__ import annotations

from fastapi import APIRouter, File, Query, UploadFile
from fastapi.responses import FileResponse

from ..core.config import get_settings
from ..schemas.common import ApiResponse, success_response
from ..schemas.task import AskRequest, TaskRequest
from ..services.file_service import FileService
from ..services.log_service import LogService
from ..services.task_service import TaskService

router = APIRouter()
settings = get_settings()
file_service = FileService(settings=settings)
log_service = LogService(settings=settings)
task_service = TaskService(file_service=file_service, log_service=log_service)


@router.get("/health", response_model=ApiResponse)
def health_check() -> ApiResponse:
    return success_response(
        {
            "status": "ok",
            "app_name": settings.app_name,
            "environment": settings.app_env,
            "model_provider": settings.model_provider,
            "use_mock_model": settings.use_mock_model,
        }
    )


@router.post("/upload", response_model=ApiResponse)
async def upload_document(file: UploadFile = File(...)) -> ApiResponse:
    content = await file.read()
    result = file_service.save_upload(file.filename or "", content)
    return success_response({"metadata": result.model_dump()})


@router.get("/files/{file_id}/content")
def get_uploaded_file_content(file_id: str) -> FileResponse:
    metadata = file_service.get_document_metadata(file_id)
    file_path = file_service.get_upload_path(file_id)
    media_type = file_service.get_upload_media_type(file_id)
    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=metadata.original_name,
        content_disposition_type="inline",
    )


@router.post("/ask", response_model=ApiResponse)
def ask_document(payload: AskRequest) -> ApiResponse:
    result = task_service.run_task(
        task_type="ask",
        endpoint="/api/ask",
        file_id=payload.file_id,
        user_input=payload.question,
        response_detail_level=payload.response_detail_level,
    )
    return success_response(result.model_dump(), request_id=result.request_id)


@router.post("/summary", response_model=ApiResponse)
def summarize_document(payload: TaskRequest) -> ApiResponse:
    result = task_service.run_task(
        task_type="summary",
        endpoint="/api/summary",
        file_id=payload.file_id,
        user_input=payload.instruction,
        response_detail_level=payload.response_detail_level,
    )
    return success_response(result.model_dump(), request_id=result.request_id)


@router.post("/outline", response_model=ApiResponse)
def outline_document(payload: TaskRequest) -> ApiResponse:
    result = task_service.run_task(
        task_type="outline",
        endpoint="/api/outline",
        file_id=payload.file_id,
        user_input=payload.instruction,
        response_detail_level=payload.response_detail_level,
    )
    return success_response(result.model_dump(), request_id=result.request_id)


@router.get("/logs", response_model=ApiResponse)
def recent_logs(limit: int = Query(default=20, ge=1, le=100)) -> ApiResponse:
    return success_response({"items": log_service.list_logs(limit=limit)})


@router.get("/logs/summary", response_model=ApiResponse)
def logs_summary(limit: int | None = Query(default=None, ge=1, le=1000)) -> ApiResponse:
    return success_response(log_service.summarize_logs(limit=limit))
