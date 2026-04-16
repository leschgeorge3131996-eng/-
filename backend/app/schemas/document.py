from __future__ import annotations

from pydantic import BaseModel


class ParsedPage(BaseModel):
    page_number: int
    text: str
    char_count: int


class ParsedDocument(BaseModel):
    file_type: str
    text: str
    page_count: int
    pages: list[ParsedPage]


class ParsedChunk(BaseModel):
    chunk_id: str
    chunk_index: int = 0
    page_numbers: list[int]
    text: str
    char_count: int


class ChunkedDocument(BaseModel):
    file_type: str
    page_count: int
    chunk_count: int
    chunks: list[ParsedChunk]


class DocumentMetadata(BaseModel):
    file_id: str
    original_name: str
    access_token: str | None = None
    owner_session_id: str | None = None
    saved_path: str
    parsed_path: str
    parsed_structure_path: str | None = None
    chunk_structure_path: str | None = None
    document_fingerprint: str | None = None
    file_type: str
    size_bytes: int
    text_chars: int = 0
    page_count: int = 0
    chunk_count: int = 0
    created_at: str
    expires_at: str | None = None
    parse_status: str
    parse_error: str | None = None


class UploadResponseData(BaseModel):
    file_id: str
    original_name: str
    access_token: str | None = None
    file_type: str
    size_bytes: int
    text_chars: int
    page_count: int
    chunk_count: int
    document_fingerprint: str | None = None
    expires_at: str | None = None
    parse_status: str
