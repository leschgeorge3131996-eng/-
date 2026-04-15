from __future__ import annotations

import hashlib
import re

from ..schemas.document import ChunkedDocument, ParsedChunk, ParsedDocument


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
            paragraphs = self._split_paragraphs(page.text)
            if not paragraphs:
                paragraphs = [page.text]

            current = ""
            for paragraph in paragraphs:
                if len(paragraph) > self.target_chunk_chars:
                    if current:
                        chunks.append(self._make_chunk(current, [page.page_number]))
                        current = ""
                    chunks.extend(self._split_long_text(paragraph, page.page_number))
                    continue

                if not current:
                    current = paragraph
                    continue

                candidate = f"{current}\n\n{paragraph}"
                if len(candidate) <= self.target_chunk_chars:
                    current = candidate
                else:
                    chunks.append(self._make_chunk(current, [page.page_number]))
                    current = paragraph

            if current:
                chunks.append(self._make_chunk(current, [page.page_number]))

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

    def _split_paragraphs(self, text: str) -> list[str]:
        return [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]

    def _split_long_text(self, text: str, page_number: int) -> list[ParsedChunk]:
        parts: list[ParsedChunk] = []
        cursor = 0
        while cursor < len(text):
            next_cursor = min(len(text), cursor + self.long_text_step)
            part = text[cursor:next_cursor].strip()
            if part:
                parts.append(self._make_chunk(part, [page_number]))
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
                merged.append(self._make_chunk(merged_text, previous.page_numbers))
            else:
                merged.append(chunk)
        return merged

    def _make_chunk(self, text: str, page_numbers: list[int]) -> ParsedChunk:
        clean_text = text.strip()
        return ParsedChunk(
            chunk_id="pending",
            chunk_index=0,
            page_numbers=page_numbers,
            text=clean_text,
            char_count=len(clean_text),
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
