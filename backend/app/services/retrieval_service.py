from __future__ import annotations

import re

from ..schemas.document import ChunkedDocument, ParsedChunk


class RetrievalService:
    def __init__(
        self,
        *,
        top_k: int = 4,
        max_context_chars: int = 3200,
        min_score: float = 1.0,
    ) -> None:
        self.top_k = top_k
        self.max_context_chars = max_context_chars
        self.min_score = min_score

    def retrieve(self, query: str, chunked_document: ChunkedDocument) -> list[ParsedChunk]:
        scored: list[tuple[float, ParsedChunk]] = []
        for chunk in chunked_document.chunks:
            score = self._score_chunk(query, chunk.text)
            if score >= self.min_score:
                scored.append((score, chunk))

        if not scored:
            return []

        scored.sort(
            key=lambda item: (
                -item[0],
                item[1].page_numbers[0] if item[1].page_numbers else 0,
                -item[1].char_count,
            )
        )
        selected: list[ParsedChunk] = []
        current_chars = 0
        for _, chunk in scored:
            if len(selected) >= self.top_k:
                break
            if current_chars + chunk.char_count > self.max_context_chars and selected:
                break
            selected.append(chunk)
            current_chars += chunk.char_count
        return selected

    def build_context(self, query: str, chunked_document: ChunkedDocument) -> tuple[list[ParsedChunk], str]:
        selected = self.retrieve(query, chunked_document)
        context = "\n\n".join(
            f"【Chunk {index} | Pages {','.join(str(page) for page in chunk.page_numbers)}】\n{chunk.text}"
            for index, chunk in enumerate(selected, start=1)
        )
        return selected, context

    def _score_chunk(self, query: str, text: str) -> float:
        normalized_text = text.lower()
        normalized_query = query.lower().strip()
        score = 0.0
        if normalized_query and normalized_query in normalized_text:
            score += 8.0

        for term in self._extract_terms(query):
            if term in normalized_text:
                weight = 2.0 if len(term) >= 3 else 1.0
                score += normalized_text.count(term) * weight
        return score

    def _extract_terms(self, query: str) -> list[str]:
        terms: list[str] = []
        for token in re.findall(r"[A-Za-z0-9]+|[\u4e00-\u9fff]+", query.lower()):
            if not token:
                continue
            if re.fullmatch(r"[\u4e00-\u9fff]+", token):
                terms.append(token)
                if len(token) >= 2:
                    terms.extend(token[index : index + 2] for index in range(len(token) - 1))
                if len(token) >= 3:
                    terms.extend(token[index : index + 3] for index in range(len(token) - 2))
            else:
                terms.append(token)

        deduped: list[str] = []
        seen: set[str] = set()
        for term in terms:
            if term not in seen:
                seen.add(term)
                deduped.append(term)
        return deduped
