from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

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

    static_dir = settings.project_root / "frontend" / "dist"
    if static_dir.is_dir():
        app.mount(
            "/assets",
            StaticFiles(directory=static_dir / "assets"),
            name="assets",
        )
        index_path = static_dir / "index.html"

        @app.get("/{full_path:path}", include_in_schema=False)
        async def spa_fallback(full_path: str) -> FileResponse:
            if full_path.startswith("api/"):
                raise HTTPException(status_code=404)
            candidate = static_dir / full_path
            if full_path and candidate.is_file():
                return FileResponse(candidate)
            return FileResponse(index_path)
    else:
        logger.warning("frontend/dist not found at %s; static serving disabled", static_dir)

    return app


app = create_app()
