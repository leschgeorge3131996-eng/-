from __future__ import annotations


class AppError(Exception):
    def __init__(
        self,
        message: str,
        *,
        code: str = "APP_ERROR",
        status_code: int = 400,
        details: dict | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}


class ValidationError(AppError):
    def __init__(self, message: str, *, details: dict | None = None) -> None:
        super().__init__(
            message,
            code="VALIDATION_ERROR",
            status_code=400,
            details=details,
        )


class ParseError(AppError):
    def __init__(self, message: str, *, details: dict | None = None) -> None:
        super().__init__(
            message,
            code="PARSE_ERROR",
            status_code=422,
            details=details,
        )


class NotFoundError(AppError):
    def __init__(self, message: str, *, details: dict | None = None) -> None:
        super().__init__(
            message,
            code="NOT_FOUND",
            status_code=404,
            details=details,
        )


class ModelServiceError(AppError):
    def __init__(self, message: str, *, details: dict | None = None) -> None:
        super().__init__(
            message,
            code="MODEL_SERVICE_ERROR",
            status_code=502,
            details=details,
        )

