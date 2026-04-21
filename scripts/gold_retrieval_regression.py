"""Offline regression check for the gold-sample questions against the current
retrieval/chunk pipeline (no remote model calls).

Verifies that after the b6547cc preprocessing strengthening:
- answerable Q1 retrieves chunks covering page 2 (or 3) with confident=True
- answerable Q2 retrieves chunks covering page 1 with confident=True
- refusal Q returns confident=False (retrieval_no_match upstream)
"""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.services.chunk_service import ChunkService
from backend.app.services.document_parser import DocumentParser
from backend.app.services.retrieval_service import RetrievalService


GOLD_PDF = PROJECT_ROOT / "evidence" / "samples" / "chinese_llm_spatial_eval.pdf"

CASES = [
    {
        "label": "Answerable 1",
        "query": "这篇论文主要研究了什么问题？",
        "expect_confident": True,
        "expect_pages_any_of": [2, 3],
    },
    {
        "label": "Answerable 2",
        "query": "作者最终的方法排名和总体准确率分别是多少？",
        "expect_confident": True,
        "expect_pages_any_of": [1],
    },
    {
        "label": "Refusal",
        "query": "木星有几颗卫星？",
        "expect_confident": False,
        "expect_pages_any_of": None,
    },
]


def run() -> int:
    print(f"[gold-regression] loading {GOLD_PDF.name}")
    parser = DocumentParser()
    parsed = parser.parse_document(GOLD_PDF)
    chunked = ChunkService().build_chunks(parsed)
    print(
        f"[gold-regression] parsed pages={parsed.page_count} "
        f"chunks={chunked.chunk_count}"
    )

    retrieval = RetrievalService()
    failures: list[str] = []
    for case in CASES:
        result = retrieval.retrieve_with_confidence(case["query"], chunked)
        pages = sorted({p for chunk in result.chunks for p in chunk.page_numbers})
        status = "confident" if result.confident else "no_match"
        print(
            f"\n[{case['label']}] {case['query']}"
            f"\n  status={status} top_score={result.top_score:.2f} "
            f"coverage={result.term_coverage:.2f} "
            f"chunks={len(result.chunks)} pages={pages}"
        )
        if result.confident != case["expect_confident"]:
            failures.append(
                f"{case['label']}: confident={result.confident} "
                f"expected={case['expect_confident']}"
            )
            continue
        if case["expect_pages_any_of"]:
            hit = any(p in pages for p in case["expect_pages_any_of"])
            if not hit:
                failures.append(
                    f"{case['label']}: pages {pages} missing any of "
                    f"{case['expect_pages_any_of']}"
                )

    if failures:
        print("\n[gold-regression] FAILURES:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\n[gold-regression] OK — all gold-sample retrieval cases pass")
    return 0


if __name__ == "__main__":
    sys.exit(run())
