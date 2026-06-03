"""端侧模型本机实测：延迟 / 体积（把"可下沉边缘"从口号变硬数）。

只读、离线、零云。测本地 BGE-small-zh-v1.5 ONNX 在本机 CPU 上的：
- 冷启动（首次 encode，含 lazy 载入 ORT session + tokenizer）
- 暖态单条编码延迟（中位数）
- 暖态批量编码延迟（一篇真实论文全部 chunk，中位数）
- DenseIndex.build（一篇文档建索引）耗时
- 模型权重体积

诚实护栏：本脚本输出是**本机/演示机代表值**，不外推为"任意边缘节点"；与端到端 QA 延迟（含云端生成 ~5521ms）明确区分；EmbeddingService 生产配置 intra/inter_op=1（FastAPI 并发下限线程），故为单线程延迟。

跑法：.venv/Scripts/python.exe scripts/edge_latency_probe.py
"""
from __future__ import annotations

import platform
import statistics
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
sys.path.insert(0, str(ROOT))

from app.services.embedding_service import EmbeddingService  # noqa: E402
from app.services.dense_index import DenseIndex  # noqa: E402

MODEL_DIR = ROOT / "models" / "bge-small-zh-v1.5"


def median_ms(fn, runs: int) -> float:
    xs = []
    for _ in range(runs):
        t = time.perf_counter()
        fn()
        xs.append((time.perf_counter() - t) * 1000)
    return statistics.median(xs)


def main() -> int:
    if not EmbeddingService(MODEL_DIR).is_available():
        print(f"[FAIL] 端侧模型缺失：{MODEL_DIR}")
        return 1

    # 体积
    onnx = MODEL_DIR / "onnx" / "model.onnx"
    onnx_data = MODEL_DIR / "onnx" / "model.onnx_data"
    size_mb = (onnx.stat().st_size + (onnx_data.stat().st_size if onnx_data.exists() else 0)) / 1024 / 1024

    # 取一篇真实论文的 chunk 文本作批量样本
    from app.schemas.document import ParsedDocument, ParsedPage
    from app.services.chunk_service import ChunkService
    import fitz

    pdf = ROOT / "evidence/samples/chinese_llm_spatial_eval.pdf"
    doc = fitz.open(pdf)
    pages = [ParsedPage(page_number=i + 1, text=p.get_text(), char_count=len(p.get_text())) for i, p in enumerate(doc)]
    parsed = ParsedDocument(file_type="pdf", text="\n".join(p.text for p in pages), page_count=len(pages), pages=pages)
    chunked = ChunkService().build_chunks(parsed)
    chunk_texts = [c.text for c in chunked.chunks]

    # 冷启动：全新 service 首次 encode（含载入）
    cold = EmbeddingService(MODEL_DIR)
    t = time.perf_counter()
    cold.encode_one("冷启动测试")
    cold_ms = (time.perf_counter() - t) * 1000

    # 暖态（复用已载入的 service）
    warm = cold
    single_ms = median_ms(lambda: warm.encode_one("这是一条用于测延迟的查询语句"), runs=20)
    batch_ms = median_ms(lambda: warm.encode(chunk_texts), runs=5)
    per_chunk_ms = batch_ms / max(1, len(chunk_texts))

    # DenseIndex.build（用临时目录）
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        di = DenseIndex(Path(tmp), warm)
        build_ms = median_ms(lambda: di.build("probe", chunked), runs=3)

    print("=" * 60)
    print("端侧模型本机实测（edge_latency_probe）")
    print("=" * 60)
    print(f"机器           : {platform.processor() or platform.machine()} · {__import__('os').cpu_count()} 逻辑核 · {platform.system()}")
    print(f"模型           : BGE-small-zh-v1.5 ONNX · 512 维 · 纯 CPU · 零云依赖 · intra/inter_op=1（单线程）")
    print(f"权重体积       : {size_mb:.1f} MB")
    print(f"测试文档       : {pdf.name}（{len(chunked.chunks)} chunk）")
    print("-" * 60)
    print(f"冷启动(首次 encode，含载入) : {cold_ms:.0f} ms")
    print(f"暖态单条编码(中位/20)       : {single_ms:.1f} ms")
    print(f"暖态批量编码 {len(chunk_texts)} chunk(中位/5) : {batch_ms:.0f} ms（≈ {per_chunk_ms:.1f} ms/chunk）")
    print(f"DenseIndex.build 全文(中位/3): {build_ms:.0f} ms")
    print("-" * 60)
    print("诚实口径：以上为本机/演示机 CPU 单线程代表值，非'任意边缘节点'通用结论；")
    print("与端到端 QA 延迟(含云端生成 ~5521ms)是两回事；端侧只做编码+检索、零云。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
