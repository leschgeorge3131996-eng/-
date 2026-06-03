"""云端 embedding 适配器：用无问芯穹 /embeddings（如 bge-m3）替换本地 BGE-small，做对照实验。

接口与 backend EmbeddingService 一致（encode / encode_one / is_available / warmup /
model_version），DenseIndex 鸭子类型直接复用。**仅用于 bge-small vs bge-m3 对照**——
注意：走云端 API ≠ 本地零云依赖，若 bge-m3 明显更好，再下其本地 ONNX 版替换端侧。
"""
from __future__ import annotations

import json
import urllib.request
import numpy as np


class CloudEmbeddingService:
    def __init__(self, settings, model: str = "bge-m3", dim: int = 1024, batch: int = 32) -> None:
        self.settings = settings
        self.model = model
        self._dim = dim
        self._batch = batch

    @property
    def model_version(self) -> str:
        return f"{self.model}-cloud-v1"  # 与本地 bge-small 版本号不同 → 旧索引自动作废重建

    def is_available(self) -> bool:
        return bool(self.settings.wuqiong_base_url and self.settings.wuqiong_api_key)

    def _embed_batch(self, batch: list[str]) -> list[list[float]]:
        url = self.settings.wuqiong_base_url.rstrip("/") + "/embeddings"
        payload = {"model": self.model, "input": batch}
        last = None
        for _ in range(3):
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                    headers={"Authorization": f"Bearer {self.settings.wuqiong_api_key}", "Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=90) as r:
                    d = json.loads(r.read().decode("utf-8", "ignore"))
                # 按 index 排序，确保与输入顺序对齐
                items = sorted(d["data"], key=lambda x: x.get("index", 0))
                return [it["embedding"] for it in items]
            except Exception as exc:  # noqa: BLE001
                last = exc
        raise last or RuntimeError("embeddings call failed")

    def encode(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, self._dim), dtype=np.float32)
        out: list[list[float]] = []
        for i in range(0, len(texts), self._batch):
            out.extend(self._embed_batch(list(texts[i : i + self._batch])))
        arr = np.asarray(out, dtype=np.float32)
        norms = np.linalg.norm(arr, axis=1, keepdims=True)
        return arr / np.clip(norms, 1e-9, None)

    def encode_one(self, text: str) -> np.ndarray:
        return self.encode([text])[0]

    def warmup(self) -> bool:
        try:
            self.encode(["预热"])
            return True
        except Exception:
            return False
