from __future__ import annotations

import re
from pathlib import Path

from ..core.exceptions import ParseError

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover
    PdfReader = None


class DocumentParser:
    supported_suffixes = {".txt", ".md", ".pdf"}

    def extract_text(self, file_path: Path) -> str:
        suffix = file_path.suffix.lower()
        if suffix not in self.supported_suffixes:
            raise ParseError(f"暂不支持的文件类型: {suffix}")

        if suffix in {".txt", ".md"}:
            return self._read_text_file(file_path)
        if suffix == ".pdf":
            return self._read_pdf(file_path)
        raise ParseError(f"无法解析的文件类型: {suffix}")

    def _read_text_file(self, file_path: Path) -> str:
        raw_bytes = file_path.read_bytes()
        for encoding in ("utf-8", "utf-8-sig", "gb18030", "gbk"):
            try:
                return self._normalize_text(raw_bytes.decode(encoding))
            except UnicodeDecodeError:
                continue
        raise ParseError("文本文件编码无法识别，请使用 UTF-8 或 GBK 编码。")

    def _read_pdf(self, file_path: Path) -> str:
        if PdfReader is None:
            raise ParseError("缺少 pypdf 依赖，无法解析 PDF。")

        try:
            reader = PdfReader(str(file_path))
            page_texts: list[str] = []
            for index, page in enumerate(reader.pages, start=1):
                extracted = (page.extract_text() or "").strip()
                if extracted:
                    page_texts.append(f"[Page {index}]\n{extracted}")
        except ParseError:
            raise
        except Exception as exc:
            raise ParseError(f"PDF 解析失败：{exc}") from exc

        if not page_texts:
            raise ParseError("PDF 未提取到有效文本，请检查文件是否为扫描件。")

        return self._normalize_text("\n\n".join(page_texts))

    def _normalize_text(self, text: str) -> str:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()
