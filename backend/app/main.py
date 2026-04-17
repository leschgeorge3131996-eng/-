from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .api.routes import router
from .core.config import get_settings
from .core.csrf import OriginValidationMiddleware
from .core.exceptions import AppError
from .core.logging_config import setup_logging
from .schemas.common import error_response

setup_logging()
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.add_middleware(
        OriginValidationMiddleware,
        allowed_origins=settings.cors_origins,
        api_prefix=settings.api_prefix,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router, prefix=settings.api_prefix)

    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
        response = error_response(
            exc.code,
            exc.message,
            details=exc.details or None,
        )
        return JSONResponse(status_code=exc.status_code, content=response.model_dump())

    @app.exception_handler(Exception)
    async def unexpected_error_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled server error")
        response = error_response(
            "INTERNAL_SERVER_ERROR",
            "服务内部发生未预期错误。",
            details={"error": str(exc)},
        )
        return JSONResponse(status_code=500, content=response.model_dump())

    return app


app = create_app()

