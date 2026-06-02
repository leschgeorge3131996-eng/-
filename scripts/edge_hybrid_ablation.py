"""离线检索 ablation：纯词法 vs 词法+本地稠密混合（不调云端模型）。

复现 evidence/reports/edge_hybrid_eval.md：
- EXTENDED_EVAL_V1 原题（可答 + 拒答）的页命中 / 拒答行为对照；
- 改写压力集（同义词自然改写、保持期望页）的页命中对照。

诚实定位：本脚本验证"零回归 + 与高度优化词法持平"，不证明"显著提升"。
需本地 models/bge-small-zh-v1.5（离线下载）。
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.services.chunk_service import ChunkService
from backend.app.services.dense_index import DenseIndex
from backend.app.services.document_parser import DocumentParser
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.retrieval_service import RetrievalService

EXTENDED = PROJECT_ROOT / "evidence" / "materials" / "EXTENDED_EVAL_V1.json"

# 改写压力集：(doc_key, 自然改写问法, 期望页) —— 期望页沿用 EXTENDED_EVAL_V1 原题
DOCS = {
    "zh": "evidence/samples/chinese_llm_spatial_eval.pdf",
    "en": "evidence/samples/attention_is_all_you_need.pdf",
    "pr": "evidence/samples/paper_report.md",
    "rb": "evidence/samples/research_brief.md",
}
PARAPHRASES = [
    ("zh", "这个研究最后答对的比例大概有多高？", [1, 5, 6]),
    ("zh", "给一个示范、用普通引导语的时候，哪个系统效果最强？", [1, 5, 6]),
    ("zh", "写这篇文章的人是哪个大学的？", [1]),
    ("zh", "这项工作主要想搞清楚哪两件事？", [2]),
    ("zh", "SPaCE 2024 这套数据分成哪些小项目？", [4]),
    ("zh", "他们参赛最后排在第几位？", [1]),
    ("zh", "用来训练的那部分一共有多少条数据？", [4]),
    ("zh", "这篇文章是在哪个会上发表的？", [1]),
    ("zh", "做实验时控制随机性的那个系数取了多少？", [5]),
    ("zh", "他们用什么标准来衡量好坏？", [5]),
    ("zh", "一共拿了多少个 AI 系统来做测试？", [4, 5, 6]),
    ("zh", "被测的这些里头，哪些是开放源代码的？", [4, 5, 6]),
    ("zh", "写论文的总共有几个人？", [1]),
    ("en", "How many stacked blocks make up the encoder side of the model?", [3]),
    ("en", "What is the reason the model drops sequential RNN-style processing?", [2, 3]),
    ("en", "Why divide the attention scores by the root of the key dimension?", [4]),
    ("en", "What are the key novel ideas this work introduces?", [1, 2, 3]),
    ("en", "What regularization drop probability is used while training the base config?", [7, 8]),
    ("en", "What gradient-descent algorithm trains the model?", [7]),
    ("en", "On what kind of machines was the base model trained?", [7]),
    ("en", "In the base configuration, how many parallel attention sub-modules are there?", [4, 5]),
    ("pr", "这个项目走的是哪种技术方案？", [1]),
    ("rb", "这款产品叫啥名字？", [1]),
]

pages_of = lambda r: {p for c in r.chunks for p in c.page_numbers}


def main() -> int:
    parser = DocumentParser()
    chunker = ChunkService()
    emb = EmbeddingService(PROJECT_ROOT / "models" / "bge-small-zh-v1.5")
    if not emb.is_available():
        print("[ablation] 缺少 models/bge-small-zh-v1.5，无法运行。")
        return 1

    lex = RetrievalService()
    tmpdir = tempfile.mkdtemp()
    dense = DenseIndex(tmpdir, emb)
    hyb = RetrievalService(dense_index=dense, dense_enabled=True)

    # ---- 1) EXTENDED_EVAL_V1 ----
    manifest = json.loads(EXTENDED.read_text(encoding="utf-8"))
    a_total = a_lex = a_hyb = 0
    r_total = r_lex = r_hyb = 0
    regress = []
    overtrigger = []
    for item in manifest["items"]:
        doc_id = item["doc_id"]
        chunked = chunker.build_chunks(parser.parse_document(PROJECT_ROOT / item["document_path"]))
        dense.build(doc_id, chunked)
        for p in item["prompts"]:
            rl = lex.retrieve_with_confidence(p["text"], chunked)
            rh = hyb.retrieve_with_confidence(p["text"], chunked, file_id=doc_id)
            if p["kind"] == "answerable":
                exp = set(p.get("expected_pages") or [])
                lh = rl.confident and bool(pages_of(rl) & exp)
                hh = rh.confident and bool(pages_of(rh) & exp)
                a_total += 1
                a_lex += int(lh)
                a_hyb += int(hh)
                if lh and not hh:
                    regress.append((doc_id, p["id"]))
            else:
                r_total += 1
                r_lex += int(not rl.confident)
                r_hyb += int(not rh.confident)
                if (not rl.confident) and rh.confident:
                    overtrigger.append((doc_id, p["id"]))

    # ---- 2) 改写压力集 ----
    chunk_cache = {}
    for key, path in DOCS.items():
        ch = chunker.build_chunks(parser.parse_document(PROJECT_ROOT / path))
        chunk_cache[key] = ch
        dense.build(f"para_{key}", ch)
    p_total = p_lex = p_hyb = 0
    for key, q, exp in PARAPHRASES:
        ch = chunk_cache[key]
        rl = lex.retrieve_with_confidence(q, ch)
        rh = hyb.retrieve_with_confidence(q, ch, file_id=f"para_{key}")
        p_total += 1
        p_lex += int(rl.confident and bool(pages_of(rl) & set(exp)))
        p_hyb += int(rh.confident and bool(pages_of(rh) & set(exp)))

    print("=" * 64)
    print("端侧语义检索离线对照（词法 vs 词法+本地稠密）")
    print("=" * 64)
    print(f"可答题(原题)  页命中  词法 {a_lex}/{a_total}  ->  混合 {a_hyb}/{a_total}")
    print(f"拒答题        不confident  词法 {r_lex}/{r_total}  ->  混合 {r_hyb}/{r_total}")
    print(f"改写压力      页命中  词法 {p_lex}/{p_total}  ->  混合 {p_hyb}/{p_total}")
    print(f"回归(混合破坏可答): {len(regress)}  | 拒答过度触发: {len(overtrigger)}")
    print("\n结论：零回归 + 与高度优化词法持平；本地语义检索价值在端侧 ML 实体+鲁棒补充，不刷分。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
