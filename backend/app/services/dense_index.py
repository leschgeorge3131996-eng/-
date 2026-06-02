"""按文档持久化的稠密向量索引（近端语义检索的存储层）。

每个文档存一个 ``{file_id}.npz``：
- ``vectors``  (N, D) float32  —— 各 chunk 的句向量（与下方 chunk_ids 顺序对齐）
- ``chunk_ids`` (N,)            —— 各向量对应的 chunk_id（chunk_id 是内容哈希，做完整性校验）
- ``model_version``            —— 编码模型版本，换模型后旧索引自动作废

完整性（吸收外部审阅意见）：检索时只采用"既在索引、又仍存在于当前文档"的 chunk_id；
任一 chunk 文本改动会改变其 chunk_id → 自动失配丢弃，绝不会把向量对错位置。

懒建：检索时若索引缺失则就地构建一次（一次性成本），避开"上传时同步编码阻塞 UI"。
"""
from __future__ import annotations

import logging
from pathlib import Path

import numpy as np

from ..schemas.document import ChunkedDocument
from .embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


class DenseIndex:
    def __init__(self, vectors_dir: str | Path, embedding_service: EmbeddingService) -> None:
        self.vectors_dir = Path(vectors_dir)
        self.embedding_service = embedding_service

    def _path(self, file_id: str) -> Path:
        return self.vectors_dir / f"{file_id}.npz"

    def exists(self, file_id: str) -> bool:
        return self._path(file_id).exists()

    def build(self, file_id: str, chunked_document: ChunkedDocument) -> bool:
        """为一个文档构建并落盘向量索引；空文档或失败返回 False（不抛给调用方）。"""
        chunks = chunked_document.chunks
        if not chunks:
            return False
        try:
            vectors = self.embedding_service.encode([chunk.text for chunk in chunks])
            chunk_ids = np.array([chunk.chunk_id for chunk in chunks], dtype=object)
            self.vectors_dir.mkdir(parents=True, exist_ok=True)
            final_path = self._path(file_id)
            # 临时名必须以 .npz 结尾，否则 np.savez 会再补一个 .npz 后缀
            tmp_path = final_path.with_name(f"{final_path.stem}.building.npz")
            np.savez(
                tmp_path,
                vectors=vectors.astype(np.float32),
                chunk_ids=chunk_ids,
                model_version=np.array(self.embedding_service.model_version),
            )
            tmp_path.replace(final_path)  # 原子替换，避免半截文件
            return True
        except Exception:
            logger.warning("稠密索引构建失败 file_id=%s", file_id, exc_info=True)
            return False

    def delete(self, file_id: str) -> None:
        path = self._path(file_id)
        try:
            if path.exists():
                path.unlink()
        except Exception:
            logger.warning("稠密索引删除失败 file_id=%s", file_id, exc_info=True)

    def score(
        self,
        query: str,
        chunked_document: ChunkedDocument,
        file_id: str,
    ) -> dict[str, float]:
        """返回 {chunk_id: 余弦相似度}（向量已归一，点积即余弦）。

        索引缺失则懒建一次；失败、模型版本不符、或文档已变，统一返回 {} → 上层回退纯词法。
        只返回"仍存在于当前文档"的 chunk_id（完整性）。
        """
        if not chunked_document.chunks:
            return {}
        path = self._path(file_id)
        if not path.exists():
            if not self.build(file_id, chunked_document):
                return {}
        try:
            with np.load(path, allow_pickle=True) as data:
                if str(data["model_version"]) != self.embedding_service.model_version:
                    return {}
                stored_ids = [str(cid) for cid in data["chunk_ids"].tolist()]
                vectors = np.asarray(data["vectors"], dtype=np.float32)
        except Exception:
            logger.warning("稠密索引读取失败 file_id=%s", file_id, exc_info=True)
            return {}

        if vectors.shape[0] != len(stored_ids) or vectors.shape[0] == 0:
            return {}

        try:
            query_vec = self.embedding_service.encode_one(query)
        except Exception:
            logger.warning("查询编码失败 file_id=%s", file_id, exc_info=True)
            return {}

        sims = vectors @ query_vec  # 两边均 L2 归一 → 点积 = 余弦
        current_ids = {chunk.chunk_id for chunk in chunked_document.chunks}
        scores: dict[str, float] = {}
        for chunk_id, sim in zip(stored_ids, sims):
            if chunk_id in current_ids:
                # 同一 chunk_id 取最高分（防御性：极少数情况下可能重复）
                value = float(sim)
                if value > scores.get(chunk_id, float("-inf")):
                    scores[chunk_id] = value
        return scores
