from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from ..core.config import Settings, get_settings
from ..core.exceptions import UnauthorizedError, ValidationError
from ..schemas.auth import CreatedSessionData, SessionData, SessionRecord


class AuthService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def create_session(
        self,
        invite_code: str,
        *,
        display_name: str | None = None,
    ) -> CreatedSessionData:
        normalized_code = invite_code.strip()
        if not normalized_code:
            raise ValidationError("邀请码不能为空。")
        if not self._is_valid_invite_code(normalized_code):
            raise UnauthorizedError("邀请码无效，请检查后重试。")

        return self._issue_session(display_name=display_name)

    def create_demo_session(
        self,
        *,
        display_name: str | None = None,
    ) -> CreatedSessionData:
        if not self.settings.demo_mode:
            raise UnauthorizedError("演示模式未启用。")
        return self._issue_session(display_name=display_name, label_prefix="demo")

    def _issue_session(
        self,
        *,
        display_name: str | None = None,
        label_prefix: str = "alpha",
    ) -> CreatedSessionData:
        self.cleanup_expired_sessions()
        created_at = datetime.now(timezone.utc)
        expires_at = created_at + timedelta(hours=self.settings.session_retention_hours)
        session_id = uuid4().hex
        session_token = f"{session_id}.{secrets.token_urlsafe(24)}"
        session_record = SessionRecord(
            session_id=session_id,
            session_token_hash=self._hash_session_token(session_token),
            label=self._build_session_label(display_name, session_id, prefix=label_prefix),
            created_at=created_at.isoformat(),
            expires_at=expires_at.isoformat(),
        )
        self._write_session_record(session_record)
        return CreatedSessionData(
            session_token=session_token,
            session=self._to_session_data(session_record),
        )

    def get_session(self, session_token: str) -> SessionData:
        session_record = self._load_session_record(session_token)
        if self._is_expired(session_record):
            self._delete_session_record(session_record.session_id)
            raise UnauthorizedError("当前试用会话已失效，请重新登录。")
        return self._to_session_data(session_record)

    def revoke_session(self, session_token: str) -> None:
        session_record = self._load_session_record(session_token)
        self._delete_session_record(session_record.session_id)

    def cleanup_expired_sessions(self, *, now: datetime | None = None) -> list[str]:
        current_time = now or datetime.now(timezone.utc)
        deleted_ids: list[str] = []
        for session_path in sorted(self.settings.sessions_dir.glob("*.json")):
            session_record = SessionRecord.model_validate_json(
                session_path.read_text(encoding="utf-8")
            )
            if current_time < datetime.fromisoformat(session_record.expires_at):
                continue
            self._delete_session_record(session_record.session_id)
            deleted_ids.append(session_record.session_id)
        return deleted_ids

    def _load_session_record(self, session_token: str) -> SessionRecord:
        normalized_token = session_token.strip()
        if not normalized_token or "." not in normalized_token:
            raise UnauthorizedError("当前试用会话无效，请重新登录。")
        session_id = normalized_token.split(".", 1)[0]
        session_path = self.settings.sessions_dir / f"{session_id}.json"
        if not session_path.exists():
            raise UnauthorizedError("当前试用会话不存在或已失效，请重新登录。")

        session_record = SessionRecord.model_validate_json(
            session_path.read_text(encoding="utf-8")
        )
        expected_hash = self._hash_session_token(normalized_token)
        if not secrets.compare_digest(session_record.session_token_hash, expected_hash):
            raise UnauthorizedError("当前试用会话无效，请重新登录。")
        return session_record

    def _write_session_record(self, session_record: SessionRecord) -> None:
        session_path = self.settings.sessions_dir / f"{session_record.session_id}.json"
        session_path.write_text(session_record.model_dump_json(indent=2), encoding="utf-8")

    def _delete_session_record(self, session_id: str) -> None:
        session_path = self.settings.sessions_dir / f"{session_id}.json"
        if session_path.exists():
            session_path.unlink()

    def _to_session_data(self, session_record: SessionRecord) -> SessionData:
        return SessionData(
            session_id=session_record.session_id,
            label=session_record.label,
            created_at=session_record.created_at,
            expires_at=session_record.expires_at,
        )

    def _hash_session_token(self, session_token: str) -> str:
        return hashlib.sha256(session_token.encode("utf-8")).hexdigest()

    def _is_valid_invite_code(self, invite_code: str) -> bool:
        return any(
            secrets.compare_digest(candidate, invite_code)
            for candidate in self.settings.alpha_invite_codes
        )

    def _build_session_label(
        self,
        display_name: str | None,
        session_id: str,
        *,
        prefix: str = "alpha",
    ) -> str:
        normalized_name = (display_name or "").strip()
        if normalized_name:
            return normalized_name[:40]
        return f"{prefix}-{session_id[:6]}"

    def _is_expired(self, session_record: SessionRecord) -> bool:
        return datetime.now(timezone.utc) >= datetime.fromisoformat(session_record.expires_at)
