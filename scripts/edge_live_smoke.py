"""端侧语义检索 —— 真实运行时端到端自检（演示机可复跑的"端侧实体"证明）。

为什么需要它：现场演示计划是把 ``EDGE_EMBEDDING_ENABLED=true`` 打开来展示端侧实体。
单元测试用的是打桩的嵌入；离线消融脚本是另写的逻辑。两者都没有证明
"本机真把 ONNX 模型加载起来、真编码、真建索引、真在检索里起作用、缺模型真回退"。
这个脚本驱动**生产代码里同一批服务类**（EmbeddingService / DenseIndex / RetrievalService），
按 routes.py 的接线方式跑一遍，逐条 PASS/FAIL 自检，任一失败 exit 1。

跑法（在仓库根）：
    .venv/Scripts/python.exe scripts/edge_live_smoke.py

它**不需要云端**：端侧实体（编码 + 混合检索）整段在本机 CPU 跑完，
云端只负责最终生成——这正是"端云协同"里能下沉到端的那部分。
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

# Windows 控制台默认 GBK，UTF-8 输出（中文 + 记号）会崩；统一切 UTF-8。
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from app.schemas.document import ParsedDocument, ParsedPage  # noqa: E402
from app.services.chunk_service import ChunkService  # noqa: E402
from app.services.dense_index import DenseIndex  # noqa: E402
from app.services.embedding_service import EmbeddingService  # noqa: E402
from app.services.retrieval_service import RetrievalService  # noqa: E402

MODEL_DIR = REPO_ROOT / "models" / "bge-small-zh-v1.5"

_failures: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    mark = "PASS" if ok else "FAIL"
    line = f"[{mark}] {name}"
    if detail:
        line += f"  —  {detail}"
    print(line)
    if not ok:
        _failures.append(name)
    return ok


def cos(a, b) -> float:
    import numpy as np

    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def build_sample_doc() -> tuple[ChunkService, "ChunkedDocument"]:
    """构造一份跨页中文文档，过真实切块管线 → 真实 chunk_id。"""
    pages = [
        ParsedPage(
            page_number=1,
            text=(
                "光合作用是绿色植物利用光能的基础过程。"
                "植物的叶绿体吸收太阳光，把二氧化碳和水合成为葡萄糖等有机物，"
                "同时向空气中释放氧气。这一过程为地球上几乎所有生命提供能量来源。\n\n"
                "叶绿素是参与光能捕获的核心色素，主要吸收红光和蓝紫光。"
            ),
            char_count=120,
        ),
        ParsedPage(
            page_number=2,
            text=(
                "细胞呼吸是生物体获取能量的另一条途径，与光合作用方向相反。"
                "线粒体把葡萄糖逐步氧化分解，释放其中储存的化学能，"
                "供细胞的各项生命活动使用，最终产物是二氧化碳和水。\n\n"
                "有氧呼吸的产能效率远高于无氧发酵。"
            ),
            char_count=110,
        ),
    ]
    full_text = "\n\n".join(p.text for p in pages)
    parsed = ParsedDocument(file_type="md", text=full_text, page_count=2, pages=pages)
    chunker = ChunkService()
    return chunker, chunker.build_chunks(parsed)


def main() -> int:
    print("=" * 64)
    print("端侧语义检索 · 真实运行时自检 (edge_live_smoke)")
    print("模型目录:", MODEL_DIR)
    print("=" * 64)

    # ---- 1. ML 实体：本机真加载 + 真编码 ----------------------------------
    emb = EmbeddingService(MODEL_DIR)
    check("1.1 端侧模型权重在本机 (is_available)", emb.is_available(),
          f"{MODEL_DIR}")
    if not emb.is_available():
        print("\n模型缺失，无法继续 ML 检查。演示机请先离线下载权重 "
              "(onnx-community/bge-small-zh-v1.5-ONNX)。")
        return 1

    check("1.2 预热成功 (warmup, 真载入 ORT session)", emb.warmup() is True)

    vecs = emb.encode([
        "植物如何把阳光变成养分",      # query-ish
        "光合作用让植物利用光能制造有机物并放出氧气",  # 语义相关
        "线粒体通过氧化分解释放化学能",                # 语义无关(呼吸)
    ])
    import numpy as np

    check("1.3 编码维度正确 (N=3, D=512)", vecs.shape == (3, 512), str(vecs.shape))
    norms = np.linalg.norm(vecs, axis=1)
    check("1.4 输出已 L2 归一 (‖v‖≈1)", bool(np.allclose(norms, 1.0, atol=1e-3)),
          f"norms={np.round(norms, 4).tolist()}")
    sim_related = cos(vecs[0], vecs[1])
    sim_unrelated = cos(vecs[0], vecs[2])
    check("1.5 语义可分：相关 > 无关", sim_related > sim_unrelated + 0.03,
          f"相关={sim_related:.3f}  无关={sim_unrelated:.3f}  Δ={sim_related - sim_unrelated:+.3f}")

    # ---- 2. 索引：真建盘 + 真读回 + 完整性 --------------------------------
    chunker, doc = build_sample_doc()
    check("2.1 真实切块产出 chunk (含内容哈希 chunk_id)", len(doc.chunks) >= 2,
          f"{len(doc.chunks)} chunks, ids={[c.chunk_id for c in doc.chunks]}")

    with tempfile.TemporaryDirectory() as tmp:
        vectors_dir = Path(tmp) / "vectors"
        index = DenseIndex(vectors_dir, emb)
        file_id = "smoke_doc"

        built = index.build(file_id, doc)
        check("2.2 稠密索引落盘 (build → .npz)", built is True)
        npz_path = vectors_dir / f"{file_id}.npz"
        check("2.3 .npz 物理存在 (np.savez 临时名补丁生效)", npz_path.exists(),
              str(npz_path))

        q_photo = "绿叶利用太阳光制造养分的生化过程"
        scores = index.score(q_photo, doc, file_id)
        check("2.4 score 返回真实 chunk_id 余弦", len(scores) == len(doc.chunks),
              f"{ {k: round(v, 3) for k, v in scores.items()} }")
        # 光合作用那一段应当排在呼吸作用那一段前面
        photo_chunk = max(doc.chunks, key=lambda c: ("光合" in c.text) or ("叶绿" in c.text))
        resp_chunk = next((c for c in doc.chunks if "呼吸" in c.text or "线粒体" in c.text), None)
        if resp_chunk is not None and photo_chunk.chunk_id in scores and resp_chunk.chunk_id in scores:
            check("2.5 语义排序正确：光合段 > 呼吸段",
                  scores[photo_chunk.chunk_id] > scores[resp_chunk.chunk_id],
                  f"光合={scores[photo_chunk.chunk_id]:.3f}  呼吸={scores[resp_chunk.chunk_id]:.3f}")

        # ---- 3. 集成：dense_enabled 检索真起作用 vs 纯词法 ---------------
        rs_dense = RetrievalService(dense_index=index, dense_enabled=True)
        rs_lex = RetrievalService()  # 默认纯词法，模拟未启用/回退

        # 一个与光合作用段几乎无字面重合的改写问法
        paraphrase = "绿叶把阳光转成养分时还会吐出什么气体"
        lex_only = rs_lex.retrieve(paraphrase, doc)  # 无 file_id → 不可能走 dense
        dense_hit = rs_dense.retrieve(paraphrase, doc, file_id=file_id)

        check("3.1 dense 检索不崩、返回结果", isinstance(dense_hit, list) and len(dense_hit) >= 1,
              f"dense={len(dense_hit)} chunk(s), lexical={len(lex_only)} chunk(s)")
        target_in_dense = any(c.chunk_id == photo_chunk.chunk_id for c in dense_hit)
        check("3.2 端侧语义把目标段召回", target_in_dense,
              "改写问法下光合段进入检索结果")
        # 诚实记录：若纯词法此例本就召回，则不夸大"救援"；只要 dense 不回归即可
        if not any(c.chunk_id == photo_chunk.chunk_id for c in lex_only):
            check("3.3 端侧语义补召回（纯词法此例漏掉，dense 补上）", target_in_dense,
                  "demonstrated rescue on a lexical miss")
        else:
            print("[INFO] 3.3 纯词法此例已命中目标段，dense 为持平/增强（不夸大救援）")

    # ---- 4. 缺模型优雅回退（现场不崩） -----------------------------------
    missing = EmbeddingService(REPO_ROOT / "models" / "__does_not_exist__")
    check("4.1 缺模型 is_available=False", missing.is_available() is False)
    # 模拟 routes 接线：不可用 → 纯词法 RetrievalService
    rs_fallback = RetrievalService() if not missing.is_available() else None
    fb = rs_fallback.retrieve("光合作用释放什么气体", doc) if rs_fallback else []
    check("4.2 回退纯词法仍能检索 (不崩)", isinstance(fb, list) and len(fb) >= 1,
          f"{len(fb)} chunk(s)")

    print("=" * 64)
    if _failures:
        print(f"结果：FAIL（{len(_failures)} 项未通过）→ {_failures}")
        return 1
    print("结果：全部通过 [OK]  端侧实体在本机真实可跑（加载/编码/建索引/检索/回退）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
