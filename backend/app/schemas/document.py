from __future__ import annotations

from pydantic import BaseModel


class DocumentMetadata(BaseModel):
    file_id: str
    original_name: str
    saved_path: str
    parsed_path: str
    file_type: str
    size_bytes: int
    text_chars: int = 0
    created_at: str
    parse_status: str
    parse_error: str | None = None


class UploadResponseData(BaseModel):
    file_id: str
    original_name: str
    file_type: str
    size_bytes: int
    text_chars: int
    parse_status: str

