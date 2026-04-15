from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ErrorPayload(BaseModel):
    code: str
    message: str
    details: dict[str, Any] | None = None


class ApiResponse(BaseModel):
    success: bool = True
    data: Any | None = None
    error: ErrorPayload | None = None
    request_id: str | None = None


def success_response(data: Any, *, request_id: str | None = None) -> ApiResponse:
    return ApiResponse(success=True, data=data, request_id=request_id)


def error_response(
    code: str,
    message: str,
    *,
    request_id: str | None = None,
    details: dict[str, Any] | None = None,
) -> ApiResponse:
    return ApiResponse(
        success=False,
        error=ErrorPayload(code=code, message=message, details=details),
        request_id=request_id,
    )

