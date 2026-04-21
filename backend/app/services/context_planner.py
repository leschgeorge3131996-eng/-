from __future__ import annotations

import re
from dataclasses import dataclass

from ..schemas.document import ChunkedDocument, ParsedChunk
from ..schemas.task import TaskType
from .retrieval_service import RetrievalResult, RetrievalService


@dataclass(slots=True)
class PlannedContext:
    strategy: str
    document_text: str
    selected_chunks: list[ParsedChunk]
    retrieval_confident: bool = True


class ContextPlannerService:
    def __init__(self, retrieval_service: RetrievalService | None = None) -> None:
        self.retrieval_service = retrieval_service or RetrievalService()

    def plan(
        self,
        *,
        task_type: TaskType,
        user_input: str | None,
        raw_text: str,
        chunked_document: ChunkedDocument,
    ) -> PlannedContext:
        if task_type == "ask":
            return self._plan_for_ask(user_input or "", raw_text, chunked_document)
        if task_type == "summary":
            return self._plan_for_summary(
                user_input=user_input or "",
                raw_text=raw_text,
                chunked_document=chunked_document,
            )
        if task_type == "outline":
            return self._plan_for_outline(
                user_input=user_input or "",
                raw_text=raw_text,
                chunked_document=chunked_document,
            )
        return PlannedContext(strategy="full_text", document_text=raw_text, selected_chunks=[])

    def _plan_for_ask(
        self,
        query: str,
        raw_text: str,
        chunked_document: ChunkedDocument,
    ) -> PlannedContext:
        result = self.retrieval_service.retrieve_with_confidence(query, chunked_document)
        if not result.chunks:
            return PlannedContext(
                strategy="no_match",
                document_text="",
                selected_chunks=[],
                retrieval_confident=False,
            )
        context = "\n\n".join(
            f"【Chunk {chunk.chunk_id} | Pages {','.join(str(page) for page in chunk.page_numbers)}】\n{chunk.text}"
            for chunk in result.chunks
        )
        return PlannedContext(
            strategy="retrieval_topk",
            document_text=context,
            selected_chunks=result.chunks,
            retrieval_confident=result.confident,
        )

    def _plan_for_summary(
        self,
        *,
        user_input: str,
        raw_text: str,
        chunked_document: ChunkedDocument,
    ) -> PlannedContext:
        return self._plan_with_intent(
            user_input=user_input,
            raw_text=raw_text,
            chunked_document=chunked_document,
            strategy="coverage_summary",
            target_chunks=6,
            max_context_chars=4200,
            relevant_quota=2,
        )

    def _plan_for_outline(
        self,
        *,
        user_input: str,
        raw_text: str,
        chunked_document: ChunkedDocument,
    ) -> PlannedContext:
        return self._plan_with_intent(
            user_input=user_input,
            raw_text=raw_text,
            chunked_document=chunked_document,
            strategy="coverage_outline",
            target_chunks=7,
            max_context_chars=4500,
            relevant_quota=3,
        )

    def _plan_with_intent(
        self,
        *,
        user_input: str,
        raw_text: str,
        chunked_document: ChunkedDocument,
        strategy: str,
        target_chunks: int,
        max_context_chars: int,
        relevant_quota: int,
    ) -> PlannedContext:
        if not chunked_document.chunks:
            return PlannedContext(strategy="full_text", document_text=raw_text, selected_chunks=[])

        coverage_indexes = self._coverage_indexes(chunked_document, target_chunks)
        relevant_chunks = (
            self.retrieval_service.retrieve(user_input, chunked_document)[:relevant_quota]
            if user_input.strip()
            else []
        )

        selected_chunks: list[ParsedChunk] = []
        current_chars = 0
        selected_ids: set[str] = set()

        for index in coverage_indexes:
            chunk = chunked_document.chunks[index]
            if current_chars + chunk.char_count > max_context_chars and selected_chunks:
                continue
            selected_chunks.append(chunk)
            selected_ids.add(chunk.chunk_id)
            current_chars += chunk.char_count
            if len(selected_chunks) >= max(2, target_chunks - relevant_quota):
                break

        for chunk in relevant_chunks:
            if chunk.chunk_id in selected_ids:
                continue
            if current_chars + chunk.char_count > max_context_chars and selected_chunks:
                continue
            selected_chunks.append(chunk)
            selected_ids.add(chunk.chunk_id)
            current_chars += chunk.char_count
            if len(selected_chunks) >= target_chunks:
                break

        if len(selected_chunks) < target_chunks:
            for index in coverage_indexes:
                chunk = chunked_document.chunks[index]
                if chunk.chunk_id in selected_ids:
                    continue
                if current_chars + chunk.char_count > max_context_chars and selected_chunks:
                    continue
                selected_chunks.append(chunk)
                selected_ids.add(chunk.chunk_id)
                current_chars += chunk.char_count
                if len(selected_chunks) >= target_chunks:
                    break

        if not selected_chunks:
            return PlannedContext(strategy="full_text", document_text=raw_text, selected_chunks=[])

        ordered_chunks = sorted(
            selected_chunks,
            key=lambda chunk: (
                chunk.page_numbers[0] if chunk.page_numbers else 0,
                chunk.chunk_index,
            ),
        )
        rendered = self._render_chunks(ordered_chunks)
        return PlannedContext(strategy=strategy, document_text=rendered, selected_chunks=ordered_chunks)

    def _plan_for_coverage(
        self,
        *,
        raw_text: str,
        chunked_document: ChunkedDocument,
        strategy: str,
        target_chunks: int,
        max_context_chars: int,
        prefer_headings: bool,
    ) -> PlannedContext:
        if not chunked_document.chunks:
            return PlannedContext(strategy="full_text", document_text=raw_text, selected_chunks=[])

        indexes: list[int] = []
        self._push_index(indexes, 0)
        self._push_index(indexes, len(chunked_document.chunks) - 1)

        if prefer_headings:
            for index, chunk in enumerate(chunked_document.chunks):
                if self._looks_like_heading_chunk(chunk.text):
                    self._push_index(indexes, index)
                if len(indexes) >= target_chunks:
                    break

        if len(indexes) < target_chunks:
            step = max(1, len(chunked_document.chunks) // target_chunks)
            for index in range(0, len(chunked_document.chunks), step):
                self._push_index(indexes, index)
                if len(indexes) >= target_chunks:
                    break

        selected_chunks: list[ParsedChunk] = []
        current_chars = 0
        for index in sorted(indexes):
            chunk = chunked_document.chunks[index]
            if current_chars + chunk.char_count > max_context_chars and selected_chunks:
                break
            selected_chunks.append(chunk)
            current_chars += chunk.char_count

        if not selected_chunks:
            return PlannedContext(strategy="full_text", document_text=raw_text, selected_chunks=[])

        rendered = self._render_chunks(selected_chunks)
        return PlannedContext(strategy=strategy, document_text=rendered, selected_chunks=selected_chunks)

    def _coverage_indexes(self, chunked_document: ChunkedDocument, target_chunks: int) -> list[int]:
        indexes: list[int] = []
        self._push_index(indexes, 0)
        self._push_index(indexes, len(chunked_document.chunks) - 1)

        for index, chunk in enumerate(chunked_document.chunks):
            if self._looks_like_heading_chunk(chunk.text):
                self._push_index(indexes, index)
            if len(indexes) >= target_chunks:
                break

        if len(indexes) < target_chunks:
            step = max(1, len(chunked_document.chunks) // target_chunks)
            for index in range(0, len(chunked_document.chunks), step):
                self._push_index(indexes, index)
                if len(indexes) >= target_chunks:
                    break

        return indexes

    def _render_chunks(self, chunks: list[ParsedChunk]) -> str:
        return "\n\n".join(
            f"【Chunk {index} | Pages {','.join(str(page) for page in chunk.page_numbers)}】\n{chunk.text}"
            for index, chunk in enumerate(chunks, start=1)
        )

    def _looks_like_heading_chunk(self, text: str) -> bool:
        stripped = text.strip()
        first_line = stripped.splitlines()[0] if stripped else ""
        if not first_line:
            return False
        if first_line.startswith("#"):
            return True
        if first_line.startswith("[Page "):
            return False
        if first_line.endswith(("。", "，", "；", "：", ".", ",", ";", ":")):
            return False
        if re.match(r"^\d+(\.\d+)*[\s、.]?", first_line):
            return True
        return len(first_line) <= 18 and len(stripped) <= 80

    def _push_index(self, indexes: list[int], value: int) -> None:
        if value not in indexes and value >= 0:
            indexes.append(value)
