from __future__ import annotations

from dataclasses import dataclass

from ..schemas.document import ChunkedDocument, ParsedChunk
from ..schemas.task import TaskType
from .retrieval_service import RetrievalService


@dataclass(slots=True)
class PlannedContext:
    strategy: str
    document_text: str
    selected_chunks: list[ParsedChunk]


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
            return self._plan_for_coverage(
                raw_text=raw_text,
                chunked_document=chunked_document,
                strategy="coverage_summary",
                target_chunks=6,
                max_context_chars=4200,
                prefer_headings=True,
            )
        if task_type == "outline":
            return self._plan_for_coverage(
                raw_text=raw_text,
                chunked_document=chunked_document,
                strategy="coverage_outline",
                target_chunks=7,
                max_context_chars=4500,
                prefer_headings=True,
            )
        return PlannedContext(strategy="full_text", document_text=raw_text, selected_chunks=[])

    def _plan_for_ask(
        self,
        query: str,
        raw_text: str,
        chunked_document: ChunkedDocument,
    ) -> PlannedContext:
        selected_chunks, retrieval_context = self.retrieval_service.build_context(query, chunked_document)
        if not selected_chunks:
            return PlannedContext(
                strategy="no_match",
                document_text="",
                selected_chunks=[],
            )
        return PlannedContext(
            strategy="retrieval_topk",
            document_text=retrieval_context,
            selected_chunks=selected_chunks,
        )

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

    def _render_chunks(self, chunks: list[ParsedChunk]) -> str:
        return "\n\n".join(
            f"【Chunk {index} | Pages {','.join(str(page) for page in chunk.page_numbers)}】\n{chunk.text}"
            for index, chunk in enumerate(chunks, start=1)
        )

    def _looks_like_heading_chunk(self, text: str) -> bool:
        stripped = text.strip()
        first_line = stripped.splitlines()[0] if stripped else ""
        return first_line.startswith("#") or (len(first_line) <= 24 and len(stripped) <= 120)

    def _push_index(self, indexes: list[int], value: int) -> None:
        if value not in indexes and value >= 0:
            indexes.append(value)
