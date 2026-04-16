from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


def _load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        os.environ.setdefault(key, value)


def _to_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _to_int(value: str | None, default: int) -> int:
    if value is None:
        return default
    return int(value)


def _to_list(value: str | None, default: list[str]) -> list[str]:
    if value is None or not value.strip():
        return default
    return [item.strip() for item in value.split(",") if item.strip()]


def _to_path(value: str | None, default: Path, base_dir: Path) -> Path:
    if value is None or not value.strip():
        return default

    candidate = Path(value).expanduser()
    if candidate.is_absolute():
        return candidate
    return (base_dir / candidate).resolve()


def _to_same_site(value: str | None, default: str) -> str:
    if value is None or not value.strip():
        return default
    normalized = value.strip().lower()
    if normalized in {"lax", "strict", "none"}:
        return normalized
    return default


@dataclass(slots=True)
class Settings:
    project_root: Path
    app_name: str
    app_env: str
    api_prefix: str
    cors_origins: list[str]
    log_level: str
    max_upload_mb: int
    max_document_chars: int
    request_timeout_seconds: int
    document_retention_hours: int
    session_retention_hours: int
    session_cookie_name: str
    session_cookie_secure: bool
    session_cookie_samesite: str
    alpha_invite_codes: list[str]
    demo_mode: bool
    data_dir: Path
    uploads_dir: Path
    parsed_dir: Path
    sessions_dir: Path
    logs_dir: Path
    cache_dir: Path
    model_provider: str
    use_mock_model: bool
    wuqiong_base_url: str
    wuqiong_api_key: str
    model_lite: str
    model_pro: str
    model_qa: str
    model_summary: str
    model_outline: str
    route_upgrade_chars: int

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024

    def ensure_directories(self) -> None:
        for path in (
            self.data_dir,
            self.uploads_dir,
            self.parsed_dir,
            self.sessions_dir,
            self.logs_dir,
            self.cache_dir,
        ):
            path.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    project_root = Path(__file__).resolve().parents[3]
    _load_env_file(project_root / ".env")

    data_dir = _to_path(os.getenv("DATA_DIR"), project_root / "data", project_root)
    settings = Settings(
        project_root=project_root,
        app_name=os.getenv("APP_NAME", "研答通"),
        app_env=os.getenv("APP_ENV", "development"),
        api_prefix="/api",
        cors_origins=_to_list(
            os.getenv("CORS_ORIGINS"),
            ["http://localhost:5173", "http://127.0.0.1:5173"],
        ),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        max_upload_mb=_to_int(os.getenv("MAX_UPLOAD_MB"), 20),
        max_document_chars=_to_int(os.getenv("MAX_DOCUMENT_CHARS"), 30000),
        request_timeout_seconds=_to_int(os.getenv("REQUEST_TIMEOUT_SECONDS"), 60),
        document_retention_hours=_to_int(os.getenv("DOCUMENT_RETENTION_HOURS"), 72),
        session_retention_hours=_to_int(os.getenv("SESSION_RETENTION_HOURS"), 168),
        session_cookie_name=os.getenv("SESSION_COOKIE_NAME", "yandatong_session"),
        session_cookie_secure=_to_bool(
            os.getenv("SESSION_COOKIE_SECURE"),
            os.getenv("APP_ENV", "development").strip().lower() == "production",
        ),
        session_cookie_samesite=_to_same_site(
            os.getenv("SESSION_COOKIE_SAMESITE"),
            "lax",
        ),
        alpha_invite_codes=_to_list(os.getenv("ALPHA_INVITE_CODES"), ["alpha-demo"]),
        demo_mode=_to_bool(os.getenv("DEMO_MODE"), False),
        data_dir=data_dir,
        uploads_dir=data_dir / "uploads",
        parsed_dir=data_dir / "parsed",
        sessions_dir=data_dir / "sessions",
        logs_dir=data_dir / "logs",
        cache_dir=data_dir / "cache",
        model_provider=os.getenv("MODEL_PROVIDER", "mock"),
        use_mock_model=_to_bool(os.getenv("USE_MOCK_MODEL"), True),
        wuqiong_base_url=os.getenv("WUQIONG_BASE_URL", "").rstrip("/"),
        wuqiong_api_key=os.getenv("WUQIONG_API_KEY", ""),
        model_lite=os.getenv("MODEL_LITE", ""),
        model_pro=os.getenv("MODEL_PRO", ""),
        model_qa=os.getenv("MODEL_QA", "placeholder-qa-model"),
        model_summary=os.getenv("MODEL_SUMMARY", "placeholder-summary-model"),
        model_outline=os.getenv("MODEL_OUTLINE", "placeholder-outline-model"),
        route_upgrade_chars=_to_int(os.getenv("ROUTE_UPGRADE_CHARS"), 12000),
    )
    settings.ensure_directories()
    return settings
