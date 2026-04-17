from __future__ import annotations

import re
from pathlib import Path

from ..core.exceptions import ParseError
from ..schemas.document import ParsedBlock, ParsedDocument, ParsedLine, ParsedPage

try:
    import pymupdf
except ImportError:  # pragma: no cover
    pymupdf = None


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
        if pymupdf is None:
            raise ParseError("缺少 pymupdf 依赖，无法解析 PDF。")

        pages: list[ParsedPage] = []
        try:
            with pymupdf.open(str(file_path)) as doc:
                for index in range(doc.page_count):
                    page = doc[index]
                    page_number = index + 1
                    width = float(page.rect.width)
                    height = float(page.rect.height)
                    raw_blocks = page.get_text("blocks") or []
                    blocks: list[ParsedBlock] = []
                    for raw in raw_blocks:
                        if len(raw) < 5:
                            continue
                        block_type = raw[6] if len(raw) >= 7 else 0
                        if block_type != 0:
                            continue
                        x0, y0, x1, y1 = float(raw[0]), float(raw[1]), float(raw[2]), float(raw[3])
                        block_text = self._normalize_text(str(raw[4]))
                        if not block_text:
                            continue
                        blocks.append(
                            ParsedBlock(text=block_text, bbox=(x0, y0, x1, y1))
                        )

                    blocks.sort(key=lambda block: (round(block.bbox[1], 1), round(block.bbox[0], 1)))

                    lines = self._extract_lines(page)

                    page_text = self._normalize_text(
                        "\n\n".join(block.text for block in blocks)
                    )
                    if not page_text and not blocks:
                        continue

                    pages.append(
                        ParsedPage(
                            page_number=page_number,
                            text=page_text,
                            char_count=len(page_text),
                            width=width,
                            height=height,
                            blocks=blocks,
                            lines=lines,
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

    def _extract_lines(self, page) -> list[ParsedLine]:
        lines: list[ParsedLine] = []
        try:
            raw_dict = page.get_text("dict") or {}
        except Exception:
            return lines

        for block in raw_dict.get("blocks", []) or []:
            if block.get("type", 0) != 0:
                continue
            for line in block.get("lines", []) or []:
                bbox_raw = line.get("bbox")
                if not bbox_raw or len(bbox_raw) < 4:
                    continue
                spans = line.get("spans", []) or []
                text = "".join(str(span.get("text", "")) for span in spans)
                normalized = self._normalize_text(text)
                if not normalized:
                    continue
                lines.append(
                    ParsedLine(
                        text=normalized,
                        bbox=(
                            float(bbox_raw[0]),
                            float(bbox_raw[1]),
                            float(bbox_raw[2]),
                            float(bbox_raw[3]),
                        ),
                    )
                )

        lines.sort(key=lambda item: (round(item.bbox[1], 1), round(item.bbox[0], 1)))
        return lines

    def _normalize_text(self, text: str) -> str:
        text = re.sub(r"[\ud800-\udfff]", "", text)
        text = text.replace("\x00", "")
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()
