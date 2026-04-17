from __future__ import annotations

import hashlib
import re

from ..schemas.document import (
    BBoxRegion,
    ChunkedDocument,
    ParsedChunk,
    ParsedDocument,
    ParsedPage,
)


class ChunkService:
    def __init__(
        self,
        *,
        target_chunk_chars: int = 900,
        min_chunk_chars: int = 250,
        long_text_step: int = 700,
    ) -> None:
        self.target_chunk_chars = target_chunk_chars
        self.min_chunk_chars = min_chunk_chars
        self.long_text_step = long_text_step

    def build_chunks(self, parsed_document: ParsedDocument) -> ChunkedDocument:
        chunks: list[ParsedChunk] = []

        for page in parsed_document.pages:
            if page.blocks:
                chunks.extend(self._chunk_from_blocks(page))
            else:
                chunks.extend(self._chunk_from_text(page))

        chunks = self._merge_small_chunks(chunks)
        chunks = [
            chunk.model_copy(
                update={
                    "chunk_index": index,
                    "chunk_id": self._stable_chunk_id(
                        text=chunk.text,
                        page_numbers=chunk.page_numbers,
                        chunk_index=index,
                    ),
                }
            )
            for index, chunk in enumerate(chunks)
        ]
        return ChunkedDocument(
            file_type=parsed_document.file_type,
            page_count=parsed_document.page_count,
            chunk_count=len(chunks),
            chunks=chunks,
        )

    def _chunk_from_blocks(self, page: ParsedPage) -> list[ParsedChunk]:
        chunks: list[ParsedChunk] = []
        current_text = ""
        current_bboxes: list[BBoxRegion] = []

        for block in page.blocks:
            block_bbox = BBoxRegion(
                page=page.page_number,
                x0=block.bbox[0],
                y0=block.bbox[1],
                x1=block.bbox[2],
                y1=block.bbox[3],
            )

            if len(block.text) > self.target_chunk_chars:
                if current_text:
                    chunks.append(
                        self._make_chunk(current_text, [page.page_number], current_bboxes)
                    )
                    current_text = ""
                    current_bboxes = []
                for sub in self._split_long_string(block.text):
                    chunks.append(
                        self._make_chunk(sub, [page.page_number], [block_bbox])
                    )
                continue

            if not current_text:
                current_text = block.text
                current_bboxes = [block_bbox]
                continue

            candidate = f"{current_text}\n\n{block.text}"
            if len(candidate) <= self.target_chunk_chars:
                current_text = candidate
                current_bboxes = current_bboxes + [block_bbox]
            else:
                chunks.append(
                    self._make_chunk(current_text, [page.page_number], current_bboxes)
                )
                current_text = block.text
                current_bboxes = [block_bbox]

        if current_text:
            chunks.append(
                self._make_chunk(current_text, [page.page_number], current_bboxes)
            )
        return chunks

    def _chunk_from_text(self, page: ParsedPage) -> list[ParsedChunk]:
        paragraphs = self._split_paragraphs(page.text)
        if not paragraphs:
            paragraphs = [page.text]

        chunks: list[ParsedChunk] = []
        current = ""
        for paragraph in paragraphs:
            if len(paragraph) > self.target_chunk_chars:
                if current:
                    chunks.append(self._make_chunk(current, [page.page_number], []))
                    current = ""
                for sub in self._split_long_string(paragraph):
                    chunks.append(self._make_chunk(sub, [page.page_number], []))
                continue

            if not current:
                current = paragraph
                continue

            candidate = f"{current}\n\n{paragraph}"
            if len(candidate) <= self.target_chunk_chars:
                current = candidate
            else:
                chunks.append(self._make_chunk(current, [page.page_number], []))
                current = paragraph

        if current:
            chunks.append(self._make_chunk(current, [page.page_number], []))
        return chunks

    def _split_paragraphs(self, text: str) -> list[str]:
        return [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]

    def _split_long_string(self, text: str) -> list[str]:
        parts: list[str] = []
        cursor = 0
        while cursor < len(text):
            next_cursor = min(len(text), cursor + self.long_text_step)
            part = text[cursor:next_cursor].strip()
            if part:
                parts.append(part)
            cursor = next_cursor
        return parts

    def _merge_small_chunks(self, chunks: list[ParsedChunk]) -> list[ParsedChunk]:
        if not chunks:
            return []

        merged: list[ParsedChunk] = []
        for chunk in chunks:
            if (
                merged
                and chunk.char_count < self.min_chunk_chars
                and merged[-1].page_numbers == chunk.page_numbers
            ):
                previous = merged.pop()
                merged_text = f"{previous.text}\n\n{chunk.text}".strip()
                merged_bboxes = previous.bbox_regions + chunk.bbox_regions
                merged.append(
                    self._make_chunk(merged_text, previous.page_numbers, merged_bboxes)
                )
            else:
                merged.append(chunk)
        return merged

    def _make_chunk(
        self,
        text: str,
        page_numbers: list[int],
        bbox_regions: list[BBoxRegion],
    ) -> ParsedChunk:
        clean_text = text.strip()
        return ParsedChunk(
            chunk_id="pending",
            chunk_index=0,
            page_numbers=page_numbers,
            text=clean_text,
            char_count=len(clean_text),
            bbox_regions=list(bbox_regions),
        )

    def _stable_chunk_id(
        self,
        *,
        text: str,
        page_numbers: list[int],
        chunk_index: int,
    ) -> str:
        chunk_key = "::".join(
            [
                ",".join(str(page) for page in page_numbers),
                str(chunk_index),
                text.strip(),
            ]
        )
        return hashlib.sha1(chunk_key.encode("utf-8")).hexdigest()[:16]
