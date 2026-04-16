from __future__ import annotations

import hashlib
import json
import mimetypes
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from ..core.config import Settings, get_settings
from ..core.exceptions import NotFoundError, ParseError, ValidationError
from ..schemas.document import (
    ChunkedDocument,
    DocumentMetadata,
    ParsedDocument,
    ParsedPage,
    UploadResponseData,
)
from .chunk_service import ChunkService
from .document_parser import DocumentParser


class FileService:
    def __init__(
        self,
        settings: Settings | None = None,
        parser: DocumentParser | None = None,
        chunk_service: ChunkService | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.parser = parser or DocumentParser()
        self.chunk_service = chunk_service or ChunkService()

    def save_upload(self, filename: str, content: bytes) -> UploadResponseData:
        if not filename:
            raise ValidationError("上传文件缺少文件名。")
        if not content:
            raise ValidationError("上传文件为空。")
        if len(content) > self.settings.max_upload_bytes:
            raise ValidationError(
                f"文件大小超过限制，当前最大支持 {self.settings.max_upload_mb}MB。"
            )

        suffix = Path(filename).suffix.lower()
        if suffix not in self.parser.supported_suffixes:
            raise ValidationError("仅支持 TXT、Markdown 和 PDF 文件。")

        file_id = uuid4().hex
        created_at = datetime.now(timezone.utc).isoformat()
        upload_path = self.settings.uploads_dir / f"{file_id}{suffix}"
        parsed_path = self.settings.parsed_dir / f"{file_id}.txt"
        parsed_structure_path = self.settings.parsed_dir / f"{file_id}.pages.json"
        chunk_structure_path = self.settings.parsed_dir / f"{file_id}.chunks.json"
        metadata_path = self.settings.parsed_dir / f"{file_id}.json"
        upload_path.write_bytes(content)

        metadata = DocumentMetadata(
            file_id=file_id,
            original_name=filename,
            saved_path=str(upload_path),
            parsed_path=str(parsed_path),
            parsed_structure_path=str(parsed_structure_path),
            chunk_structure_path=str(chunk_structure_path),
            document_fingerprint=None,
            file_type=suffix.lstrip("."),
            size_bytes=len(content),
            text_chars=0,
            page_count=0,
            chunk_count=0,
            created_at=created_at,
            parse_status="pending",
        )

        try:
            parsed_document = self.parser.parse_document(upload_path)
            if not parsed_document.text:
                raise ParseError("文档未提取到有效文本。")
            chunked_document = self.chunk_service.build_chunks(parsed_document)
            parsed_path.write_text(parsed_document.text, encoding="utf-8")
            self._write_structure(parsed_structure_path, parsed_document)
            self._write_chunks(chunk_structure_path, chunked_document)
            metadata.parse_status = "parsed"
            metadata.text_chars = len(parsed_document.text)
            metadata.page_count = parsed_document.page_count
            metadata.chunk_count = chunked_document.chunk_count
            metadata.document_fingerprint = self._build_document_fingerprint(parsed_document.text)
        except ParseError as exc:
            metadata.parse_status = "failed"
            metadata.parse_error = exc.message
            self._write_metadata(metadata_path, metadata)
            raise
        except Exception as exc:
            metadata.parse_status = "failed"
            metadata.parse_error = str(exc)
            self._write_metadata(metadata_path, metadata)
            raise ParseError(f"文档解析失败：{exc}") from exc

        self._write_metadata(metadata_path, metadata)
        return UploadResponseData(
            file_id=metadata.file_id,
            original_name=metadata.original_name,
            file_type=metadata.file_type,
            size_bytes=metadata.size_bytes,
            text_chars=metadata.text_chars,
            page_count=metadata.page_count,
            chunk_count=metadata.chunk_count,
            document_fingerprint=metadata.document_fingerprint,
            parse_status=metadata.parse_status,
        )

    def get_document_text(self, file_id: str) -> str:
        parsed_path = self.settings.parsed_dir / f"{file_id}.txt"
        if not parsed_path.exists():
            raise NotFoundError("未找到对应的解析文本，请先重新上传文件。")
        return parsed_path.read_text(encoding="utf-8")

    def get_document_metadata(self, file_id: str) -> DocumentMetadata:
        metadata_path = self.settings.parsed_dir / f"{file_id}.json"
        if not metadata_path.exists():
            raise NotFoundError("未找到对应的文档元数据。")
        return DocumentMetadata.model_validate_json(metadata_path.read_text(encoding="utf-8"))

    def get_document_structure(self, file_id: str) -> ParsedDocument:
        structure_path = self.settings.parsed_dir / f"{file_id}.pages.json"
        if not structure_path.exists():
            raise NotFoundError("未找到对应的结构化解析结果。")
        return ParsedDocument.model_validate_json(structure_path.read_text(encoding="utf-8"))

    def get_document_chunks(self, file_id: str) -> ChunkedDocument:
        chunk_path = self.settings.parsed_dir / f"{file_id}.chunks.json"
        if not chunk_path.exists():
            raise NotFoundError("未找到对应的文档分块结果。")
        return ChunkedDocument.model_validate_json(chunk_path.read_text(encoding="utf-8"))

    def get_document_page(self, file_id: str, page_number: int) -> ParsedPage:
        structure = self.get_document_structure(file_id)
        for page in structure.pages:
            if page.page_number == page_number:
                return page
        raise NotFoundError("未找到对应的页面内容。")

    def get_upload_path(self, file_id: str) -> Path:
        metadata = self.get_document_metadata(file_id)
        upload_path = Path(metadata.saved_path)
        if not upload_path.exists():
            raise NotFoundError("原始文件不存在，请重新上传文档。")
        return upload_path

    def get_upload_media_type(self, file_id: str) -> str:
        metadata = self.get_document_metadata(file_id)
        guessed_type, _ = mimetypes.guess_type(metadata.original_name or metadata.saved_path)
        return guessed_type or "application/octet-stream"

    def _write_metadata(self, metadata_path: Path, metadata: DocumentMetadata) -> None:
        metadata_path.write_text(metadata.model_dump_json(indent=2), encoding="utf-8")

    def _build_document_fingerprint(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _write_structure(self, structure_path: Path, parsed_document: ParsedDocument) -> None:
        structure_path.write_text(parsed_document.model_dump_json(indent=2), encoding="utf-8")

    def _write_chunks(self, chunk_path: Path, chunked_document: ChunkedDocument) -> None:
        chunk_path.write_text(chunked_document.model_dump_json(indent=2), encoding="utf-8")
