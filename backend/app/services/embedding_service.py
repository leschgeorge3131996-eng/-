"""端侧/近端句向量编码服务（本地 ONNX，零云依赖）。

把 BGE-small-zh-v1.5 的 ONNX 模型跑在本机 CPU 上，将文本编码成归一化句向量。
这是研答通"端云协同"里真实的近端 ML 算力实体：解析/切块/检索/语义编码全部本地完成，
云端（无问芯穹 MaaS）只接收命中的必要片段做生成。

设计要点（吸收外部审阅意见）：
- 单例 lazy 加载：首次 encode 时才载入 ORT session + tokenizer，加载失败抛异常交由上层回退纯词法。
- Windows ORT 限线程（intra/inter=1），避免 FastAPI 并发下抢占。
- 直接用模型自带的 ``sentence_embedding`` 输出（= CLS 池化 + L2 归一），无池化歧义；
  若该输出不存在则回退到 last_hidden_state 的 CLS token 再归一。
"""
from __future__ import annotations

import threading
from pathlib import Path

import numpy as np

EMBEDDING_DIM = 512


class EmbeddingService:
    def __init__(self, model_dir: str | Path, *, max_threads: int = 1, max_length: int = 512) -> None:
        self.model_dir = Path(model_dir)
        self._max_threads = max(1, max_threads)
        self._max_length = max_length
        self._lock = threading.Lock()
        self._session = None
        self._tokenizer = None
        self._input_names: list[str] = []
        self._output_names: list[str] = []
        self._uses_sentence_embedding = False

    @property
    def model_version(self) -> str:
        # 用于稠密索引完整性校验：模型换了，旧向量自动作废
        return "bge-small-zh-v1.5-onnx-v1"

    def is_available(self) -> bool:
        model_path = self.model_dir / "onnx" / "model.onnx"
        tok_path = self.model_dir / "tokenizer.json"
        return model_path.exists() and tok_path.exists()

    def _ensure_loaded(self) -> None:
        if self._session is not None:
            return
        with self._lock:
            if self._session is not None:
                return
            import onnxruntime as ort  # 延迟导入：未启用时不付出导入成本
            from tokenizers import Tokenizer

            model_path = self.model_dir / "onnx" / "model.onnx"
            tok_path = self.model_dir / "tokenizer.json"
            if not model_path.exists() or not tok_path.exists():
                raise FileNotFoundError(
                    f"端侧嵌入模型缺失，期望在 {self.model_dir} 下找到 onnx/model.onnx 与 tokenizer.json"
                )

            options = ort.SessionOptions()
            options.intra_op_num_threads = self._max_threads
            options.inter_op_num_threads = 1
            session = ort.InferenceSession(
                str(model_path),
                sess_options=options,
                providers=["CPUExecutionProvider"],
            )
            tokenizer = Tokenizer.from_file(str(tok_path))
            tokenizer.enable_truncation(max_length=self._max_length)
            tokenizer.enable_padding()

            self._input_names = [i.name for i in session.get_inputs()]
            self._output_names = [o.name for o in session.get_outputs()]
            self._uses_sentence_embedding = "sentence_embedding" in self._output_names
            self._tokenizer = tokenizer
            self._session = session

    def encode(self, texts: list[str]) -> np.ndarray:
        """把一批文本编码成 (N, D) 的 L2 归一化向量；空输入返回 (0, D)。"""
        if not texts:
            return np.zeros((0, EMBEDDING_DIM), dtype=np.float32)
        self._ensure_loaded()
        assert self._tokenizer is not None and self._session is not None

        encodings = self._tokenizer.encode_batch(list(texts))
        input_ids = np.array([e.ids for e in encodings], dtype=np.int64)
        attention_mask = np.array([e.attention_mask for e in encodings], dtype=np.int64)

        feed: dict[str, np.ndarray] = {}
        for name in self._input_names:
            if name == "input_ids":
                feed[name] = input_ids
            elif name == "attention_mask":
                feed[name] = attention_mask
            elif name == "token_type_ids":
                feed[name] = np.zeros_like(input_ids)

        if self._uses_sentence_embedding:
            out = self._session.run(["sentence_embedding"], feed)[0]
        else:
            hidden = self._session.run([self._output_names[0]], feed)[0]
            out = hidden[:, 0, :]  # CLS token

        out = np.asarray(out, dtype=np.float32)
        norms = np.linalg.norm(out, axis=-1, keepdims=True)
        return out / np.clip(norms, 1e-9, None)

    def encode_one(self, text: str) -> np.ndarray:
        return self.encode([text])[0]

    def warmup(self) -> bool:
        """启动时预热一次，避免首问卡顿；失败只返回 False，绝不抛给调用方。"""
        try:
            self.encode(["预热"])
            return True
        except Exception:
            return False
