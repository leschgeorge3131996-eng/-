from __future__ import annotations

import hashlib
import mimetypes
import secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from ..core.config import Settings, get_settings
from ..core.exceptions import ForbiddenError, NotFoundError, ParseError, ValidationError
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

    def save_upload(
        self,
        filename: str,
        content: bytes,
        *,
        owner_session_id: str | None = None,
    ) -> UploadResponseData:
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
        created_at = datetime.now(timezone.utc)
        expires_at = created_at + timedelta(hours=self.settings.document_retention_hours)
        upload_path = self.settings.uploads_dir / f"{file_id}{suffix}"
        parsed_path = self.settings.parsed_dir / f"{file_id}.txt"
        parsed_structure_path = self.settings.parsed_dir / f"{file_id}.pages.json"
        chunk_structure_path = self.settings.parsed_dir / f"{file_id}.chunks.json"
        metadata_path = self.settings.parsed_dir / f"{file_id}.json"
        upload_path.write_bytes(content)

        metadata = DocumentMetadata(
            file_id=file_id,
            original_name=filename,
            access_token=self._build_access_token(),
            owner_session_id=owner_session_id,
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
            created_at=created_at.isoformat(),
            expires_at=expires_at.isoformat(),
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
        return self._to_upload_response(metadata)

    def get_document_text(
        self,
        file_id: str,
        access_token: str | None = None,
        *,
        session_id: str | None = None,
    ) -> str:
        self.get_document_metadata(
            file_id,
            access_token=access_token,
            session_id=session_id,
        )
        parsed_path = self.settings.parsed_dir / f"{file_id}.txt"
        if not parsed_path.exists():
            raise NotFoundError("未找到对应的解析文本，请先重新上传文件。")
        return parsed_path.read_text(encoding="utf-8")

    def get_document_metadata(
        self,
        file_id: str,
        access_token: str | None = None,
        *,
        require_access: bool = True,
        session_id: str | None = None,
    ) -> DocumentMetadata:
        metadata_path = self.settings.parsed_dir / f"{file_id}.json"
        if not metadata_path.exists():
            raise NotFoundError("未找到对应的文档元数据。")

        metadata = DocumentMetadata.model_validate_json(metadata_path.read_text(encoding="utf-8"))
        if require_access:
            self._assert_document_access(metadata, access_token, session_id=session_id)
        return metadata

    def get_document_structure(
        self,
        file_id: str,
        access_token: str | None = None,
        *,
        session_id: str | None = None,
    ) -> ParsedDocument:
        self.get_document_metadata(
            file_id,
            access_token=access_token,
            session_id=session_id,
        )
        structure_path = self.settings.parsed_dir / f"{file_id}.pages.json"
        if not structure_path.exists():
            raise NotFoundError("未找到对应的结构化解析结果。")
        return ParsedDocument.model_validate_json(structure_path.read_text(encoding="utf-8"))

    def get_document_chunks(
        self,
        file_id: str,
        access_token: str | None = None,
        *,
        session_id: str | None = None,
    ) -> ChunkedDocument:
        self.get_document_metadata(
            file_id,
            access_token=access_token,
            session_id=session_id,
        )
        chunk_path = self.settings.parsed_dir / f"{file_id}.chunks.json"
        if not chunk_path.exists():
            raise NotFoundError("未找到对应的文档分块结果。")
        return ChunkedDocument.model_validate_json(chunk_path.read_text(encoding="utf-8"))

    def get_document_page(
        self,
        file_id: str,
        page_number: int,
        access_token: str | None = None,
        *,
        session_id: str | None = None,
    ) -> ParsedPage:
        structure = self.get_document_structure(
            file_id,
            access_token=access_token,
            session_id=session_id,
        )
        for page in structure.pages:
            if page.page_number == page_number:
                return page
        raise NotFoundError("未找到对应的页面内容。")

    def render_document_page(
        self,
        file_id: str,
        page_number: int,
        *,
        access_token: str | None = None,
        session_id: str | None = None,
        dpi: int = 144,
    ) -> bytes:
        metadata = self.get_document_metadata(
            file_id,
            access_token=access_token,
            session_id=session_id,
        )
        if metadata.file_type != "pdf":
            raise ValidationError("仅支持 PDF 文档的页面渲染。")

        upload_path = Path(metadata.saved_path)
        if not upload_path.exists():
            raise NotFoundError("原始文件不存在，请重新上传文档。")

        try:
            import pymupdf
        except ImportError as exc:  # pragma: no cover
            raise ParseError("缺少 pymupdf 依赖，无法渲染 PDF。") from exc

        try:
            with pymupdf.open(str(upload_path)) as doc:
                if page_number < 1 or page_number > doc.page_count:
                    raise NotFoundError("未找到对应的页面内容。")
                page = doc[page_number - 1]
                pix = page.get_pixmap(dpi=dpi, alpha=False)
                return pix.tobytes("png")
        except NotFoundError:
            raise
        except Exception as exc:
            raise ParseError(f"PDF 页面渲染失败：{exc}") from exc

    def get_upload_path(
        self,
        file_id: str,
        access_token: str | None = None,
        *,
        session_id: str | None = None,
    ) -> Path:
        metadata = self.get_document_metadata(
            file_id,
            access_token=access_token,
            session_id=session_id,
        )
        upload_path = Path(metadata.saved_path)
        if not upload_path.exists():
            raise NotFoundError("原始文件不存在，请重新上传文档。")
        return upload_path

    def get_upload_media_type(
        self,
        file_id: str,
        access_token: str | None = None,
        *,
        session_id: str | None = None,
    ) -> str:
        metadata = self.get_document_metadata(
            file_id,
            access_token=access_token,
            session_id=session_id,
        )
        guessed_type, _ = mimetypes.guess_type(metadata.original_name or metadata.saved_path)
        return guessed_type or "application/octet-stream"

    def delete_document(
        self,
        file_id: str,
        access_token: str | None = None,
        *,
        session_id: str | None = None,
    ) -> UploadResponseData:
        metadata = self.get_document_metadata(
            file_id,
            access_token=access_token,
            session_id=session_id,
        )
        self._delete_document_files(metadata)
        return self._to_upload_response(metadata)

    def cleanup_expired_documents(self, *, now: datetime | None = None) -> list[str]:
        current_time = now or datetime.now(timezone.utc)
        deleted_file_ids: list[str] = []

        for metadata_path in sorted(self.settings.parsed_dir.glob("*.json")):
            if metadata_path.name.endswith(".pages.json") or metadata_path.name.endswith(".chunks.json"):
                continue

            metadata = DocumentMetadata.model_validate_json(metadata_path.read_text(encoding="utf-8"))
            if not self._is_expired(metadata, current_time):
                continue

            self._delete_document_files(metadata)
            deleted_file_ids.append(metadata.file_id)

        return deleted_file_ids

    def _to_upload_response(self, metadata: DocumentMetadata) -> UploadResponseData:
        return UploadResponseData(
            file_id=metadata.file_id,
            original_name=metadata.original_name,
            access_token=metadata.access_token,
            file_type=metadata.file_type,
            size_bytes=metadata.size_bytes,
            text_chars=metadata.text_chars,
            page_count=metadata.page_count,
            chunk_count=metadata.chunk_count,
            document_fingerprint=metadata.document_fingerprint,
            expires_at=metadata.expires_at,
            parse_status=metadata.parse_status,
        )

    def _write_metadata(self, metadata_path: Path, metadata: DocumentMetadata) -> None:
        metadata_path.write_text(metadata.model_dump_json(indent=2), encoding="utf-8")

    def _build_document_fingerprint(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _build_access_token(self) -> str:
        return secrets.token_urlsafe(24)

    def _assert_document_access(
        self,
        metadata: DocumentMetadata,
        access_token: str | None,
        *,
        session_id: str | None = None,
    ) -> None:
        if metadata.owner_session_id:
            if not session_id or not secrets.compare_digest(metadata.owner_session_id, session_id):
                raise ForbiddenError(
                    "当前试用会话无权访问该文档。",
                    details={"file_id": metadata.file_id},
                )
        if not metadata.access_token:
            return
        if access_token and secrets.compare_digest(metadata.access_token, access_token):
            return
        raise ForbiddenError(
            "当前文档访问凭证无效或已缺失。",
            details={"file_id": metadata.file_id},
        )

    def _is_expired(self, metadata: DocumentMetadata, current_time: datetime) -> bool:
        if metadata.expires_at:
            return current_time >= datetime.fromisoformat(metadata.expires_at)
        created_at = datetime.fromisoformat(metadata.created_at)
        return current_time >= created_at + timedelta(hours=self.settings.document_retention_hours)

    def _delete_document_files(self, metadata: DocumentMetadata) -> None:
        for candidate in (
            Path(metadata.saved_path),
            Path(metadata.parsed_path),
            Path(metadata.parsed_structure_path) if metadata.parsed_structure_path else None,
            Path(metadata.chunk_structure_path) if metadata.chunk_structure_path else None,
            self.settings.parsed_dir / f"{metadata.file_id}.json",
        ):
            if candidate and candidate.exists():
                candidate.unlink()

    def _write_structure(self, structure_path: Path, parsed_document: ParsedDocument) -> None:
        structure_path.write_text(parsed_document.model_dump_json(indent=2), encoding="utf-8")

    def _write_chunks(self, chunk_path: Path, chunked_document: ChunkedDocument) -> None:
        chunk_path.write_text(chunked_document.model_dump_json(indent=2), encoding="utf-8")
