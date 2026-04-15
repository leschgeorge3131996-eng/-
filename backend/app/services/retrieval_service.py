from __future__ import annotations

import re

from ..schemas.document import ChunkedDocument, ParsedChunk


class RetrievalService:
    stopwords = {
        "请",
        "帮我",
        "一下",
        "这个",
        "这个项目",
        "这份文档",
        "这篇文档",
        "这篇文章",
        "请问",
        "一下子",
        "关于",
        "一下吧",
        "the",
        "a",
        "an",
        "is",
        "are",
        "what",
        "does",
        "do",
        "about",
    }

    bilingual_query_hints = {
        "为什么": ["why", "because"],
        "放弃": ["avoid", "replace", "dispense with"],
        "循环": ["recurrent", "rnn"],
        "卷积": ["convolutional", "cnn"],
        "结构": ["architecture", "structure"],
        "核心方法": ["method", "approach", "model"],
        "创新点": ["contribution", "novel", "novelty"],
        "实验结果": ["experiment", "results"],
        "研究背景": ["background", "motivation"],
        "结论": ["conclusion"],
    }

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
        normalized_query = self._normalize_query(query)
        score = 0.0
        if normalized_query and normalized_query in normalized_text:
            score += 8.0

        normalized_terms = self._extract_terms(normalized_query)
        raw_terms = self._extract_terms(query.lower())
        terms = self._dedupe_terms(normalized_terms + raw_terms)
        title_bonus = self._title_bonus(terms, text)
        score += title_bonus

        length_norm = max(1.0, len(text) / 600)
        for term in terms:
            if term in normalized_text:
                if term in {"recurrent", "convolutional", "rnn", "cnn", "architecture", "method", "results", "background", "conclusion"}:
                    weight = 4.0
                else:
                    weight = 2.0 if len(term) >= 3 else 1.0
                score += (normalized_text.count(term) * weight) / length_norm
        return score

    def _normalize_query(self, query: str) -> str:
        normalized = re.sub(r"[^\w\u4e00-\u9fff]+", " ", query.lower()).strip()
        for stopword in sorted(self.stopwords, key=len, reverse=True):
            normalized = normalized.replace(stopword, " ")
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return normalized

    def _extract_terms(self, query: str) -> list[str]:
        terms: list[str] = []
        for token in re.findall(r"[A-Za-z0-9]+|[\u4e00-\u9fff]+", query.lower()):
            if not token:
                continue
            if token in self.stopwords:
                continue
            if re.fullmatch(r"[\u4e00-\u9fff]+", token):
                terms.append(token)
                if len(token) >= 2:
                    terms.extend(token[index : index + 2] for index in range(len(token) - 1))
                if len(token) >= 3:
                    terms.extend(token[index : index + 3] for index in range(len(token) - 2))
            else:
                terms.append(token)

        for chinese_term, english_terms in self.bilingual_query_hints.items():
            if chinese_term in query:
                terms.extend(english_terms)

        return self._dedupe_terms(terms)

    def _title_bonus(self, terms: list[str], text: str) -> float:
        if not terms:
            return 0.0
        first_line = text.strip().splitlines()[0].lower() if text.strip() else ""
        if not first_line:
            return 0.0
        bonus = 0.0
        for term in terms:
            if term in first_line:
                bonus += 1.5 if len(term) >= 3 else 0.5
        if first_line.startswith("#") or re.match(r"^\d+(\.\d+)*", first_line):
            bonus += 0.5
        return bonus

    def _dedupe_terms(self, terms: list[str]) -> list[str]:
        deduped: list[str] = []
        seen: set[str] = set()
        for term in terms:
            if term not in seen:
                seen.add(term)
                deduped.append(term)
        return deduped
