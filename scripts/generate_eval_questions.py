"""泛化测试出题器：让强模型读原文，造一批"我们没预先精选过"的全新题。

为什么：现有 123 题是人工精选的固定集，证明不了泛化。本脚本对每个文档用强模型
（默认 qwen3-235b，128k 上下文，读全文）现造题——可答题（带答案要点+页码）+ 拒答陷阱题
（文档里查无依据的、看着却能答的），输出成 EXTENDED_EVAL 的 manifest 格式，
直接喂 judged_eval.py 跑"作答→源接地判分→人复核"。

诚实护栏：生成的题/参考答案可能有噪声 → 判分用『源接地裁判』（以原文为准、不盲信生成的参考）
+ 人复核 fail + 抽查拒答陷阱是否真不可答。

跑法：
    .venv/Scripts/python.exe scripts/generate_eval_questions.py \
        --out evidence/materials/GENERALIZATION_EVAL_20260602.json \
        --answerable 8 --refusal 3
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.app.core.config import get_settings  # noqa: E402

SRC_MANIFESTS = [
    "evidence/materials/EXTENDED_EVAL_V1.json",
    "evidence/materials/HOLDOUT_EVAL_V6_EXTREME_FULL_20260430.json",
]


def doc_text(doc_path: str, cap: int = 18000) -> tuple[str, int]:
    full = ROOT / doc_path
    if full.suffix.lower() == ".pdf":
        import fitz

        d = fitz.open(full)
        pages = [p.get_text() for p in d]
        text = "\n".join(f"[p{i+1}]\n{t}" for i, t in enumerate(pages))
        return text[:cap], len(pages)
    text = full.read_text(encoding="utf-8", errors="ignore")
    return text[:cap], 1


def collect_docs() -> list[dict]:
    seen, docs = set(), []
    for mp in SRC_MANIFESTS:
        d = json.loads((ROOT / mp).read_text(encoding="utf-8"))
        for it in d["items"]:
            if it["document_path"] in seen:
                continue
            seen.add(it["document_path"])
            docs.append({"doc_id": it["doc_id"], "document_path": it["document_path"], "language": it.get("language", "zh")})
    return docs


GEN_SYS = (
    "你是资深评测出题人。读给定文档全文，产出**全新**的考察题，目标是检验问答系统的泛化能力。\n"
    "出两类题：\n"
    "A) 可答题（answerable）：答案确实能在文档中找到。覆盖事实/数字、跨段推理、表格对比、定义、总结等不同难度，"
    "尽量刁钻但有据。每题给：question、answer_keywords（正确答案里必然出现的关键片段，2-4个）、pages（支撑页码，整数数组）。\n"
    "B) 拒答陷阱题（refusal）：问一个**听上去与文档相关、但文档里根本没有依据**的细节（正确做法是拒答、不能编）。"
    "务必确保文档确实没有答案。每题只给 question。\n"
    "只输出一个 JSON：{\"answerable\":[{\"question\":\"\",\"answer_keywords\":[],\"pages\":[]}],\"refusal\":[{\"question\":\"\"}]}"
)


def gen_for_doc(settings, doc, n_ans, n_ref, gen_model):
    text, npages = doc_text(doc["document_path"])
    user = (
        f"文档（{doc['language']}，共约 {npages} 页）：\n{text}\n\n"
        f"请出 {n_ans} 道可答题 + {n_ref} 道拒答陷阱题。pages 用上面 [p#] 标的页码。只输出 JSON。"
    )
    payload = {
        "model": gen_model,
        "messages": [{"role": "system", "content": GEN_SYS}, {"role": "user", "content": user}],
        "temperature": 0.4,
        "max_tokens": 2200,
    }
    url = settings.wuqiong_base_url.rstrip("/") + "/chat/completions"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {settings.wuqiong_api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    last = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.loads(r.read().decode("utf-8", "ignore"))
            c = data["choices"][0]["message"]["content"]
            s, e = c.find("{"), c.rfind("}")
            return json.loads(c[s : e + 1])
        except Exception as exc:  # noqa: BLE001
            last = exc
    raise last or RuntimeError("gen failed")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="evidence/materials/GENERALIZATION_EVAL_20260602.json")
    ap.add_argument("--answerable", type=int, default=8)
    ap.add_argument("--refusal", type=int, default=3)
    ap.add_argument("--gen-model", default="qwen3-235b-a22b-instruct-2507")
    args = ap.parse_args()

    settings = get_settings()
    if settings.use_mock_model or not (settings.wuqiong_base_url and settings.wuqiong_api_key):
        print("[FAIL] 需要真实 MaaS 配置（.env）。")
        return 1

    docs = collect_docs()
    print(f"文档 {len(docs)} 个，出题模型 {args.gen_model}（每文档 ~{args.answerable} 可答 + {args.refusal} 拒答）")
    items, n_ans, n_ref = [], 0, 0
    for i, doc in enumerate(docs, 1):
        try:
            g = gen_for_doc(settings, doc, args.answerable, args.refusal, args.gen_model)
        except Exception as exc:  # noqa: BLE001
            print(f"[{i}/{len(docs)}] {doc['doc_id']}: 生成失败 {exc}")
            continue
        prompts = []
        for j, q in enumerate(g.get("answerable", [])):
            if not q.get("question"):
                continue
            prompts.append({
                "id": f"gen_ans_{j}",
                "text": q["question"],
                "kind": "answerable",
                "category": "GEN-A",
                "expected_any_of": [str(k) for k in (q.get("answer_keywords") or [])],
                "expected_pages": [int(p) for p in (q.get("pages") or []) if str(p).isdigit()],
                "difficulty": "medium",
            })
        for j, q in enumerate(g.get("refusal", [])):
            if not q.get("question"):
                continue
            prompts.append({
                "id": f"gen_ref_{j}",
                "text": q["question"],
                "kind": "refusal",
                "category": "GEN-R",
                "expected_any_of": [],
                "expected_pages": [],
                "difficulty": "hard",
            })
        a = sum(1 for p in prompts if p["kind"] == "answerable")
        r = sum(1 for p in prompts if p["kind"] == "refusal")
        n_ans += a
        n_ref += r
        items.append({**doc, "prompts": prompts})
        print(f"[{i}/{len(docs)}] {doc['doc_id']}: +{a} 可答 / +{r} 拒答")

    manifest = {
        "version": "generalization-1",
        "name": "Generalization eval (freshly generated, 2026-06-02)",
        "description": "强模型现造题，测系统对未精选问题的泛化；判分用源接地裁判+人复核。",
        "response_detail_level": "balanced",
        "items": items,
    }
    out = ROOT / args.out
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print("=" * 56)
    print(f"已生成 {n_ans} 可答 + {n_ref} 拒答 = {n_ans + n_ref} 题 → {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
