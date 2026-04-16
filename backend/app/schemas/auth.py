from __future__ import annotations

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    invite_code: str = Field(..., min_length=1, max_length=200)
    display_name: str | None = Field(default=None, max_length=80)


class SessionData(BaseModel):
    session_id: str
    label: str
    created_at: str
    expires_at: str


class SessionRecord(BaseModel):
    session_id: str
    session_token_hash: str
    label: str
    created_at: str
    expires_at: str


class CreatedSessionData(BaseModel):
    session_token: str
    session: SessionData


class LoginResponseData(BaseModel):
    session: SessionData
