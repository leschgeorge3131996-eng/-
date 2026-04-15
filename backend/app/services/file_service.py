from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from ..core.config import Settings, get_settings
from ..core.exceptions import NotFoundError, ParseError, ValidationError
from ..schemas.document import DocumentMetadata, UploadResponseData
from .document_parser import DocumentParser


class FileService:
    def __init__(
        self,
        settings: Settings | None = None,
        parser: DocumentParser | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.parser = parser or DocumentParser()

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
        metadata_path = self.settings.parsed_dir / f"{file_id}.json"
        upload_path.write_bytes(content)

        metadata = DocumentMetadata(
            file_id=file_id,
            original_name=filename,
            saved_path=str(upload_path),
            parsed_path=str(parsed_path),
            file_type=suffix.lstrip("."),
            size_bytes=len(content),
            text_chars=0,
            created_at=created_at,
            parse_status="pending",
        )

        try:
            text = self.parser.extract_text(upload_path)
            if not text:
                raise ParseError("文档未提取到有效文本。")
            parsed_path.write_text(text, encoding="utf-8")
            metadata.parse_status = "parsed"
            metadata.text_chars = len(text)
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

    def _write_metadata(self, metadata_path: Path, metadata: DocumentMetadata) -> None:
        metadata_path.write_text(metadata.model_dump_json(indent=2), encoding="utf-8")
