"""端侧/近端稠密检索融合单测（用桩索引，不依赖真实模型）。

覆盖三态：
- 稠密增召回：词法命中的结果之外，补进语义相关但词法没排进来的片段。
- 词法空时救援：词法零命中但语义高度相关时返回该片段并 confident=True（"换个问法"）。
- 默认/关闭：dense_enabled=False 时完全等同纯词法（零回归）。
"""
from __future__ import annotations

from backend.app.schemas.document import ChunkedDocument, ParsedChunk
from backend.app.services.retrieval_service import RetrievalService


def _doc() -> ChunkedDocument:
    texts = {
        "a": "检索增强生成框架用于学术论文问答与证据回链。",
        "b": "实验部分采用准确率、召回率与 F1 值作为主要评测指标。",
        "c": "模型在四张显卡上训练了大约三十个小时完成收敛。",
    }
    chunks = [
        ParsedChunk(chunk_id=cid, chunk_index=i, page_numbers=[i + 1], text=t, char_count=len(t))
        for i, (cid, t) in enumerate(texts.items())
    ]
    return ChunkedDocument(file_type="txt", page_count=3, chunk_count=3, chunks=chunks)


class _StubDenseIndex:
    def __init__(self, mapping: dict[str, dict[str, float]]) -> None:
        self.mapping = mapping

    def score(self, query: str, chunked_document, file_id: str) -> dict[str, float]:
        return dict(self.mapping.get(query, {}))


def test_dense_augment_adds_semantic_chunk_to_lexical_hit():
    # 词法命中 a；桩对 b 给高语义分（b 词法排不进来）-> 结果应同时含 a 与 b
    svc = RetrievalService(
        dense_index=_StubDenseIndex({"检索增强生成": {"b": 0.62}}),
        dense_enabled=True,
    )
    result = svc.retrieve_with_confidence("检索增强生成", _doc(), file_id="f1")
    ids = {chunk.chunk_id for chunk in result.chunks}
    assert "a" in ids  # 词法
    assert "b" in ids  # 稠密增召回


def test_dense_rescue_when_lexical_empty():
    # 词法零命中（无任何词重叠）；桩对 c 给 >= 救援阈值的语义分 -> 返回 c 且 confident
    svc = RetrievalService(
        dense_index=_StubDenseIndex({"紫色独角兽宇宙飞船": {"c": 0.71}}),
        dense_enabled=True,
    )
    result = svc.retrieve_with_confidence("紫色独角兽宇宙飞船", _doc(), file_id="f1")
    assert [chunk.chunk_id for chunk in result.chunks] == ["c"]
    assert result.confident is True


def test_dense_below_rescue_threshold_still_refuses():
    # 词法空 + 语义分低于救援阈值 -> 不救援，维持拒答语义
    svc = RetrievalService(
        dense_index=_StubDenseIndex({"紫色独角兽宇宙飞船": {"c": 0.30}}),
        dense_enabled=True,
    )
    result = svc.retrieve_with_confidence("紫色独角兽宇宙飞船", _doc(), file_id="f1")
    assert result.chunks == []
    assert result.confident is False


def test_dense_disabled_is_pure_lexical():
    # 关闭开关：即便桩给高分也不参与 -> 词法空仍拒答（零回归）
    svc = RetrievalService(
        dense_index=_StubDenseIndex({"紫色独角兽宇宙飞船": {"c": 0.99}}),
        dense_enabled=False,
    )
    result = svc.retrieve_with_confidence("紫色独角兽宇宙飞船", _doc(), file_id="f1")
    assert result.chunks == []
    assert result.confident is False


def test_no_file_id_skips_dense():
    # 没有 file_id 时不查稠密（即使开关打开）
    svc = RetrievalService(
        dense_index=_StubDenseIndex({"紫色独角兽宇宙飞船": {"c": 0.99}}),
        dense_enabled=True,
    )
    result = svc.retrieve_with_confidence("紫色独角兽宇宙飞船", _doc(), file_id=None)
    assert result.chunks == []
    assert result.confident is False
