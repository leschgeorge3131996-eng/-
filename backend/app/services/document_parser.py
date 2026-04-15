from __future__ import annotations

import re
from pathlib import Path

from ..core.exceptions import ParseError
from ..schemas.document import ParsedDocument, ParsedPage

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover
    PdfReader = None


class DocumentParser:
    supported_suffixes = {".txt", ".md", ".pdf"}

    def parse_document(self, file_path: Path) -> ParsedDocument:
        suffix = file_path.suffix.lower()
        if suffix not in self.supported_suffixes:
            raise ParseError(f"暂不支持的文件类型: {suffix}")

        if suffix in {".txt", ".md"}:
            text = self._read_text_file(file_path)
            return ParsedDocument(
                file_type=suffix.lstrip("."),
                text=text,
                page_count=1,
                pages=[
                    ParsedPage(
                        page_number=1,
                        text=text,
                        char_count=len(text),
                    )
                ],
            )
        if suffix == ".pdf":
            return self._read_pdf(file_path)
        raise ParseError(f"无法解析的文件类型: {suffix}")

    def extract_text(self, file_path: Path) -> str:
        return self.parse_document(file_path).text

    def _read_text_file(self, file_path: Path) -> str:
        raw_bytes = file_path.read_bytes()
        for encoding in ("utf-8", "utf-8-sig", "gb18030", "gbk"):
            try:
                return self._normalize_text(raw_bytes.decode(encoding))
            except UnicodeDecodeError:
                continue
        raise ParseError("文本文件编码无法识别，请使用 UTF-8 或 GBK 编码。")

    def _read_pdf(self, file_path: Path) -> ParsedDocument:
        if PdfReader is None:
            raise ParseError("缺少 pypdf 依赖，无法解析 PDF。")

        try:
            reader = PdfReader(str(file_path))
            pages: list[ParsedPage] = []
            for index, page in enumerate(reader.pages, start=1):
                extracted = self._normalize_text(page.extract_text() or "")
                if extracted:
                    pages.append(
                        ParsedPage(
                            page_number=index,
                            text=extracted,
                            char_count=len(extracted),
                        )
                    )
        except ParseError:
            raise
        except Exception as exc:
            raise ParseError(f"PDF 解析失败：{exc}") from exc

        if not pages:
            raise ParseError("PDF 未提取到有效文本，请检查文件是否为扫描件。")

        combined_text = self._normalize_text(
            "\n\n".join(f"[Page {page.page_number}]\n{page.text}" for page in pages)
        )
        return ParsedDocument(
            file_type="pdf",
            text=combined_text,
            page_count=len(pages),
            pages=pages,
        )

    def _normalize_text(self, text: str) -> str:
        text = re.sub(r"[\ud800-\udfff]", "", text)
        text = text.replace("\x00", "")
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()
