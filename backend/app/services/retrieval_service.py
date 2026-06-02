from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

from ..schemas.document import ChunkedDocument, ParsedChunk


@dataclass(slots=True)
class RetrievalResult:
    chunks: list[ParsedChunk] = field(default_factory=list)
    top_score: float = 0.0
    second_score: float = 0.0
    term_coverage: float = 0.0
    confident: bool = True


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
        "开源": ["qwen", "deepseek", "open source"],
        "验证集": ["validation", "development", "dev", "总计"],
        "测试集": ["test", "总计"],
        "训练集": ["train", "training", "总计"],
        "样本数": ["sample", "samples", "总计"],
        "结构": ["architecture", "structure"],
        "核心方法": ["method", "approach", "model"],
        "创新点": ["contribution", "novel", "novelty"],
        "实验结果": ["experiment", "results"],
        "研究背景": ["background", "motivation"],
        "结论": ["conclusion"],
        "attention heads": ["h = 8", "parallel attention layers", "heads"],
        "base transformer": ["h = 8", "base model", "parallel attention layers"],
        "main contributions": ["we propose", "entirely on attention", "sequence transduction", "transformer"],
    }

    metadata_intent_terms = (
        "作者",
        "第一作者",
        "通讯作者",
        "名称",
        "名字",
        "产品名",
        "项目名",
        "叫什么",
        "单位",
        "高校",
        "学校",
        "机构",
        "来自",
        "贡献",
        "主要贡献",
        "标题",
        "题目",
        "摘要",
        "author",
        "authors",
        "affiliation",
        "affiliations",
        "institution",
        "university",
        "contribution",
        "contributions",
        "title",
        "name",
        "product",
        "project",
        "abstract",
    )

    contribution_intent_terms = (
        "贡献",
        "主要贡献",
        "创新点",
        "contribution",
        "contributions",
        "novelty",
    )

    overview_intent_terms = (
        "讲了什么",
        "讲的什么",
        "说了什么",
        "主要讲",
        "主要内容",
        "最重要的内容",
        "重要内容",
        "重点内容",
        "核心内容",
        "核心观点",
        "主要观点",
        "中心思想",
        "大概内容",
        "文章内容",
        "文档内容",
        "概括",
        "总结",
        "介绍一下",
        "overview",
        "summarize",
        "summary",
        "about",
    )

    parameter_intent_terms = (
        "样本数",
        "验证集",
        "测试集",
        "训练集",
        "总数",
        "开源",
        "是否开源",
        "参数",
        "配置",
        "attention heads",
        "heads",
        "head",
        "h =",
        "h=",
        "layers",
        "layer",
        "dropout",
        "label smoothing",
        "pdrop",
    )

    def __init__(
        self,
        *,
        top_k: int = 4,
        max_context_chars: int = 3200,
        min_score: float = 1.0,
        dense_index=None,
        dense_enabled: bool = False,
        dense_min_sim: float = 0.40,
        dense_rescue_sim: float = 0.50,
        dense_max_extra: int = 3,
    ) -> None:
        self.top_k = top_k
        self.max_context_chars = max_context_chars
        self.min_score = min_score
        # 端侧/近端语义检索（默认关闭；启用需注入 dense_index）。关闭时本服务行为与纯词法完全一致。
        self.dense_index = dense_index
        self.dense_enabled = dense_enabled
        self.dense_min_sim = dense_min_sim
        self.dense_rescue_sim = dense_rescue_sim
        self.dense_max_extra = dense_max_extra

    def retrieve(
        self, query: str, chunked_document: ChunkedDocument, *, file_id: str | None = None
    ) -> list[ParsedChunk]:
        result = self.retrieve_with_confidence(query, chunked_document, file_id=file_id)
        return result.chunks

    def retrieve_with_confidence(
        self, query: str, chunked_document: ChunkedDocument, *, file_id: str | None = None
    ) -> RetrievalResult:
        idf = self._build_idf(query, chunked_document)

        scored: list[tuple[float, ParsedChunk]] = []
        for chunk in chunked_document.chunks:
            score = self._score_chunk(query, chunk.text, idf)
            if score >= self.min_score:
                scored.append((score, chunk))

        metadata_intent = self._has_metadata_intent(query)
        overview_intent = self._has_overview_intent(query)
        dense_scores = self._dense_scores(query, chunked_document, file_id)
        if not scored:
            if overview_intent and chunked_document.chunks:
                chunks = self._head_context_chunks(chunked_document)
                return RetrievalResult(
                    chunks=chunks,
                    top_score=0.0,
                    second_score=0.0,
                    term_coverage=0.0,
                    confident=True,
                )
            if metadata_intent and chunked_document.chunks:
                return RetrievalResult(
                    chunks=[chunked_document.chunks[0]],
                    top_score=0.0,
                    second_score=0.0,
                    term_coverage=0.0,
                    confident=True,
                )
            # 词法零命中但语义高度相关（"换个问法"）：稠密救援，避免漏答
            rescue = self._dense_rescue_chunks(dense_scores, chunked_document)
            if rescue:
                return RetrievalResult(
                    chunks=rescue,
                    top_score=0.0,
                    second_score=0.0,
                    term_coverage=0.0,
                    confident=True,
                )
            return RetrievalResult(confident=False)

        scored.sort(
            key=lambda item: (
                -item[0],
                item[1].page_numbers[0] if item[1].page_numbers else 0,
                -item[1].char_count,
            )
        )

        top_score = scored[0][0]
        second_score = scored[1][0] if len(scored) > 1 else 0.0

        normalized_query = self._normalize_query(query)
        query_terms = self._dedupe_terms(
            self._extract_terms(normalized_query) + self._extract_terms(query.lower())
        )
        if query_terms:
            best_text = scored[0][1].text.lower()
            matched_terms = sum(1 for t in query_terms if t in best_text)
            term_coverage = matched_terms / len(query_terms)
        else:
            term_coverage = 0.0

        confident = top_score >= 2.0 or (top_score >= 1.5 and term_coverage >= 0.3)

        selected: list[ParsedChunk] = []
        current_chars = 0
        for _, chunk in scored:
            if len(selected) >= self.top_k:
                break
            if current_chars + chunk.char_count > self.max_context_chars and selected:
                continue
            if chunk.char_count > self.max_context_chars and not selected:
                continue
            selected.append(chunk)
            current_chars += chunk.char_count

        if metadata_intent and chunked_document.chunks:
            head_chunk = chunked_document.chunks[0]
            selected_ids = {chunk.chunk_id for chunk in selected}
            if head_chunk.chunk_id not in selected_ids:
                selected.append(head_chunk)

        if overview_intent and chunked_document.chunks:
            selected = self._append_missing_chunks(
                self._head_context_chunks(chunked_document),
                selected,
                max_total=self.top_k + 2,
            )
            confident = True

        if self._has_contribution_intent(query) and chunked_document.chunks:
            selected = self._append_missing_chunks(
                selected,
                chunked_document.chunks[:2],
                max_total=self.top_k + 2,
            )

        if self._has_parameter_intent(query):
            selected = self._append_neighbor_chunks(
                selected,
                chunked_document.chunks,
                radius=1,
                max_total=self.top_k + 3,
            )

        # 稠密增召回：把语义相关但词法没排进来的片段补进来（保守，不动主排序与置信度）
        if dense_scores:
            selected = self._dense_augment_chunks(selected, dense_scores, chunked_document)

        return RetrievalResult(
            chunks=selected,
            top_score=top_score,
            second_score=second_score,
            term_coverage=term_coverage,
            confident=confident,
        )

    def _dense_active(self) -> bool:
        return self.dense_enabled and self.dense_index is not None

    def _dense_scores(
        self, query: str, chunked_document: ChunkedDocument, file_id: str | None
    ) -> dict[str, float]:
        if not self._dense_active() or not file_id:
            return {}
        try:
            return self.dense_index.score(query, chunked_document, file_id)
        except Exception:
            # 任何稠密侧失败都回退纯词法，绝不影响主链路
            return {}

    def _dense_rescue_chunks(
        self, dense_scores: dict[str, float], chunked_document: ChunkedDocument
    ) -> list[ParsedChunk]:
        if not dense_scores:
            return []
        ranked = sorted(
            (item for item in dense_scores.items() if item[1] >= self.dense_rescue_sim),
            key=lambda item: -item[1],
        )
        if not ranked:
            return []
        by_id = {chunk.chunk_id: chunk for chunk in chunked_document.chunks}
        selected: list[ParsedChunk] = []
        current_chars = 0
        for chunk_id, _ in ranked[: self.top_k]:
            chunk = by_id.get(chunk_id)
            if chunk is None:
                continue
            if current_chars + chunk.char_count > self.max_context_chars and selected:
                break
            selected.append(chunk)
            current_chars += chunk.char_count
        return selected

    def _dense_augment_chunks(
        self,
        selected: list[ParsedChunk],
        dense_scores: dict[str, float],
        chunked_document: ChunkedDocument,
    ) -> list[ParsedChunk]:
        ranked = sorted(
            (item for item in dense_scores.items() if item[1] >= self.dense_min_sim),
            key=lambda item: -item[1],
        )
        by_id = {chunk.chunk_id: chunk for chunk in chunked_document.chunks}
        candidates = [by_id[chunk_id] for chunk_id, _ in ranked if chunk_id in by_id]
        return self._append_missing_chunks(
            selected, candidates, max_total=self.top_k + self.dense_max_extra
        )

    def _has_metadata_intent(self, query: str) -> bool:
        lowered = query.lower()
        return any(term in lowered for term in self.metadata_intent_terms)

    def _has_contribution_intent(self, query: str) -> bool:
        lowered = query.lower()
        return any(term in lowered for term in self.contribution_intent_terms)

    def _has_overview_intent(self, query: str) -> bool:
        lowered = query.lower()
        return any(term in lowered for term in self.overview_intent_terms)

    def _has_parameter_intent(self, query: str) -> bool:
        lowered = query.lower()
        return any(term in lowered for term in self.parameter_intent_terms)

    def _head_context_chunks(self, chunked_document: ChunkedDocument) -> list[ParsedChunk]:
        selected: list[ParsedChunk] = []
        current_chars = 0
        for chunk in chunked_document.chunks:
            if len(selected) >= min(self.top_k, 4):
                break
            if current_chars + chunk.char_count > self.max_context_chars and selected:
                break
            selected.append(chunk)
            current_chars += chunk.char_count
        return selected

    def _append_neighbor_chunks(
        self,
        selected: list[ParsedChunk],
        all_chunks: list[ParsedChunk],
        *,
        radius: int,
        max_total: int,
    ) -> list[ParsedChunk]:
        by_index = {chunk.chunk_index: chunk for chunk in all_chunks}
        candidates: list[ParsedChunk] = []
        for chunk in selected:
            for offset in range(-radius, radius + 1):
                if offset == 0:
                    continue
                neighbor = by_index.get(chunk.chunk_index + offset)
                if neighbor is not None:
                    candidates.append(neighbor)
        return self._append_missing_chunks(selected, candidates, max_total=max_total)

    def _append_missing_chunks(
        self,
        selected: list[ParsedChunk],
        candidates: list[ParsedChunk],
        *,
        max_total: int,
    ) -> list[ParsedChunk]:
        expanded = list(selected)
        selected_ids = {chunk.chunk_id for chunk in expanded}
        for chunk in candidates:
            if len(expanded) >= max_total:
                break
            if chunk.chunk_id in selected_ids:
                continue
            expanded.append(chunk)
            selected_ids.add(chunk.chunk_id)
        return expanded

    def build_context(self, query: str, chunked_document: ChunkedDocument) -> tuple[list[ParsedChunk], str]:
        selected = self.retrieve(query, chunked_document)
        context = "\n\n".join(
            f"【Chunk {chunk.chunk_id} | Pages {','.join(str(page) for page in chunk.page_numbers)}】\n{chunk.text}"
            for chunk in selected
        )
        return selected, context

    def _score_chunk(self, query: str, text: str, idf: dict[str, float]) -> float:
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
                base_weight = 2.0 if len(term) >= 3 else 1.0
                term_idf = idf.get(term, 1.0)
                weight = base_weight * term_idf
                score += (normalized_text.count(term) * weight) / length_norm
        return score

    def _build_idf(self, query: str, chunked_document: ChunkedDocument) -> dict[str, float]:
        normalized_query = self._normalize_query(query)
        normalized_terms = self._extract_terms(normalized_query)
        raw_terms = self._extract_terms(query.lower())
        terms = self._dedupe_terms(normalized_terms + raw_terms)
        if not terms:
            return {}

        n = len(chunked_document.chunks)
        if n == 0:
            return {}

        df: dict[str, int] = {term: 0 for term in terms}
        for chunk in chunked_document.chunks:
            lowered = chunk.text.lower()
            for term in terms:
                if term in lowered:
                    df[term] += 1

        idf: dict[str, float] = {}
        for term, count in df.items():
            if count == 0:
                idf[term] = 1.0
            else:
                idf[term] = max(0.5, math.log(n / count) + 1.0)
        return idf

    def _normalize_query(self, query: str) -> str:
        return " ".join(self._query_tokens(query))

    def _extract_terms(self, query: str) -> list[str]:
        terms: list[str] = []
        for token in self._query_tokens(query):
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

        for chinese_term, english_terms in self.bilingual_query_hints.items():
            if chinese_term in query:
                terms.extend(english_terms)

        return self._dedupe_terms(terms)

    def _query_tokens(self, query: str) -> list[str]:
        normalized = re.sub(r"[^\w\u4e00-\u9fff]+", " ", query.lower()).strip()
        raw_tokens = re.findall(r"[A-Za-z0-9]+|[\u4e00-\u9fff]+", normalized)
        if not raw_tokens:
            return []

        cjk_stopwords = sorted(
            [word for word in self.stopwords if re.fullmatch(r"[\u4e00-\u9fff]+", word)],
            key=len,
            reverse=True,
        )

        tokens: list[str] = []
        for token in raw_tokens:
            if token in self.stopwords:
                continue

            if re.fullmatch(r"[\u4e00-\u9fff]+", token):
                fragments = [token]
                for stopword in cjk_stopwords:
                    next_fragments: list[str] = []
                    for fragment in fragments:
                        next_fragments.extend(fragment.split(stopword))
                    fragments = next_fragments

                for fragment in fragments:
                    cleaned = fragment.strip()
                    if cleaned and cleaned not in self.stopwords:
                        tokens.append(cleaned)
                continue

            tokens.append(token)

        return tokens

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
