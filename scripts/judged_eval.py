"""判分式评测：系统真实作答 + 强模型当裁判逐题判，再由人兜底复核。

动机：固定题集 + 自动代理指标（页码命中 / 关键词命中）有两个弱点——样本固定、
且代理指标会误判（答对但页码没对上判成 fail；答错但含关键词判成 pass）。本脚本把判分
升级为"读答案+证据+参考，逐题裁决对不对/撑不撑得住/该不该拒答"，更接近真人判分。

设计（诚实优先）：
- 答题：本项目真实链路（``deepseek-v4-flash`` + 检索回链），计费到 .env 里的账号。
- 裁判：另一个更强的模型（默认 ``qwen3-235b-a22b-instruct-2507``，与答题模型不同），
  从严裁决：证据撑不住 / 模棱两可一律判不过；拒答题给出实质答案=判不过（视为编造）。
- 兜底：脚本只产"裁判初判"，人（Claude）须复核所有 fail + 抽查 pass，最终结论人来背。

跑法：
    .venv/Scripts/python.exe scripts/judged_eval.py \
        --manifest evidence/materials/EXTENDED_EVAL_V1.json \
        --out evidence/reports/judged_eval_v1_20260602 [--limit N]
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.app.core.config import get_settings  # noqa: E402
from backend.app.services.auth_service import AuthService  # noqa: E402
from backend.app.services.file_service import FileService  # noqa: E402
from backend.app.services.log_service import LogService  # noqa: E402
from backend.app.services.model_client import ModelClient  # noqa: E402
from backend.app.services.task_service import TaskService  # noqa: E402

JUDGE_SYS = (
    "你是严格的文档问答评测裁判。判定标准：\n"
    "1) 对【可答题】：只有当系统答案在事实上正确、且能被『系统引用证据』或『参考要点』支撑时，才判 pass=true；"
    "答案含糊、与参考要点矛盾、答非所问、或证据撑不住，一律 pass=false。\n"
    "2) 对【拒答题】（文档中无依据）：系统拒答 = pass=true；系统给出了实质性答案 = pass=false（视为编造）。\n"
    "3) grounded：系统答案是否由所给引用证据支撑（拒答题填 true）。\n"
    "从严裁决：拿不准一律判 false。只输出一个 JSON，不要解释。"
)


def judge_call(settings, question, kind, reference, answer, evidence, outcome, judge_model):
    url = settings.wuqiong_base_url.rstrip("/") + "/chat/completions"
    user = (
        f"【题型】{'可答题' if kind != 'refusal' else '拒答题（文档无依据，正确做法是拒答）'}\n"
        f"【问题】{question}\n"
        f"【参考要点】{reference or '（无）'}\n"
        f"【系统是否拒答】{outcome}\n"
        f"【系统答案】{answer or '（空）'}\n"
        f"【系统引用证据】{evidence or '（无）'}\n\n"
        '只返回 JSON：{"pass": true/false, "label": "correct|partial|wrong_answer|ungrounded|'
        'correct_refusal|should_have_refused|over_refused", "grounded": true/false, "reason": "一句话"}'
    )
    payload = {
        "model": judge_model,
        "messages": [{"role": "system", "content": JUDGE_SYS}, {"role": "user", "content": user}],
        "temperature": 0,
        "max_tokens": 400,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {settings.wuqiong_api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        data = json.loads(r.read().decode("utf-8", "ignore"))
    content = data["choices"][0]["message"]["content"]
    rid = data.get("id")
    # 抽取第一个 JSON 对象
    s, e = content.find("{"), content.rfind("}")
    verdict = json.loads(content[s : e + 1])
    verdict["_judge_rid"] = rid
    return verdict


def load_cases(manifest_path: Path):
    d = json.loads(manifest_path.read_text(encoding="utf-8"))
    cases = []
    for it in d["items"]:
        for p in it.get("prompts", []):
            cases.append(
                {
                    "case_id": f"{it['doc_id']}:{p['id']}",
                    "doc_path": it["document_path"],
                    "question": p["text"],
                    "kind": p.get("kind", "answerable"),
                    "category": p.get("category"),
                    "reference": "；".join(p.get("expected_any_of", []) or []),
                }
            )
    return cases


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="evidence/materials/EXTENDED_EVAL_V1.json")
    ap.add_argument("--out", default="evidence/reports/judged_eval_20260602")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--judge-model", default="qwen3-235b-a22b-instruct-2507")
    args = ap.parse_args()

    settings = get_settings()
    if settings.use_mock_model or not (settings.wuqiong_base_url and settings.wuqiong_api_key):
        print("[FAIL] 需要真实 MaaS 配置（.env），当前是 mock 或缺 key。")
        return 1

    auth = AuthService(settings=settings)
    fs = FileService(settings=settings)
    ls = LogService(settings=settings)
    mc = ModelClient(settings=settings)
    ts = TaskService(file_service=fs, model_client=mc, log_service=ls)
    sess = auth.create_session("alpha-demo").session.session_id

    cases = load_cases(ROOT / args.manifest)
    if args.limit:
        cases = cases[: args.limit]
    print(f"题目数：{len(cases)}（答题 deepseek-v4-flash / 裁判 {args.judge_model}）")

    # 同一文档只上传一次
    uploads: dict[str, object] = {}
    records = []
    for i, c in enumerate(cases, 1):
        if c["doc_path"] not in uploads:
            pdf = ROOT / c["doc_path"]
            uploads[c["doc_path"]] = fs.save_upload(pdf.name, pdf.read_bytes(), owner_session_id=sess)
        up = uploads[c["doc_path"]]
        try:
            r = ts.run_task(
                task_type="ask",
                endpoint="/api/ask",
                file_id=up.file_id,
                session_id=sess,
                document_access_token=up.access_token,
                user_input=c["question"],
                response_detail_level="balanced",
            )
            answer = r.result
            outcome = r.outcome
            evidence = " | ".join(
                [q.quote for q in getattr(r, "evidence_quotes", [])]
                + [f"p{p}:{cit.snippet}" for cit in getattr(r, "citations", []) for p in cit.page_numbers]
            )[:1200]
            ans_rid = getattr(r, "platform_request_id", None)
        except Exception as exc:  # noqa: BLE001
            answer, outcome, evidence, ans_rid = f"(ERROR {exc})", "error", "", None

        try:
            v = judge_call(settings, c["question"], c["kind"], c["reference"], answer, evidence, outcome, args.judge_model)
        except Exception as exc:  # noqa: BLE001
            v = {"pass": False, "label": "judge_error", "grounded": False, "reason": f"裁判异常 {exc}", "_judge_rid": None}

        rec = {
            **{k: c[k] for k in ("case_id", "kind", "category", "question", "reference")},
            "answer": answer,
            "outcome": outcome,
            "evidence": evidence,
            "answer_rid": ans_rid,
            "judge_pass": bool(v.get("pass")),
            "judge_label": v.get("label"),
            "judge_grounded": bool(v.get("grounded")),
            "judge_reason": v.get("reason"),
            "judge_rid": v.get("_judge_rid"),
        }
        records.append(rec)
        mark = "PASS" if rec["judge_pass"] else "FAIL"
        print(f"[{i}/{len(cases)}] {mark} {c['kind'][:3]} {c['case_id']} — {rec['judge_label']}: {str(rec['judge_reason'])[:60]}")

    total = len(records)
    passed = sum(1 for r in records if r["judge_pass"])
    ans = [r for r in records if r["kind"] != "refusal"]
    ref = [r for r in records if r["kind"] == "refusal"]
    ans_pass = sum(1 for r in ans if r["judge_pass"])
    ref_pass = sum(1 for r in ref if r["judge_pass"])
    halluc = [r for r in records if r["kind"] == "refusal" and not r["judge_pass"]]
    label_counts: dict[str, int] = {}
    for r in records:
        label_counts[r["judge_label"]] = label_counts.get(r["judge_label"], 0) + 1

    out_json = ROOT / f"{args.out}.json"
    out_md = ROOT / f"{args.out}.md"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    summary = {
        "total": total,
        "passed": passed,
        "pass_rate": round(passed / total, 4) if total else 0,
        "answerable_total": len(ans),
        "answerable_passed": ans_pass,
        "refusal_total": len(ref),
        "refusal_passed": ref_pass,
        "hallucinated_refusals": len(halluc),
        "labels": label_counts,
        "judge_model": args.judge_model,
        "answer_model": settings.model_qa,
    }
    out_json.write_text(json.dumps({"summary": summary, "records": records}, ensure_ascii=False, indent=1), encoding="utf-8")

    fails = [r for r in records if not r["judge_pass"]]
    lines = [
        f"# 判分式评测（裁判初判）· {Path(args.manifest).stem}",
        "",
        "> 答题：`deepseek-v4-flash` + 检索回链（真实链路）。裁判：`" + args.judge_model + "`（从严，不同模型）。",
        "> **这是裁判初判，须由人复核所有 FAIL + 抽查 PASS 后才作数。**",
        "",
        "## 汇总",
        f"- 总通过：**{passed}/{total}（{summary['pass_rate']*100:.1f}%）**",
        f"- 可答题：{ans_pass}/{len(ans)}",
        f"- 拒答题：{ref_pass}/{len(ref)}（其中 {len(halluc)} 个该拒未拒=潜在编造）",
        f"- 标签分布：{label_counts}",
        "",
        "## 全部未通过（人需逐个复核）",
        "",
        "| case_id | 题型 | 标签 | 裁判理由 | 系统答案(截断) |",
        "|---|---|---|---|---|",
    ]
    for r in fails:
        lines.append(
            f"| {r['case_id']} | {r['kind']} | {r['judge_label']} | {str(r['judge_reason'])[:80]} | {str(r['answer'])[:80]} |"
        )
    out_md.write_text("\n".join(lines), encoding="utf-8")

    print("=" * 60)
    print(f"裁判初判：{passed}/{total}（{summary['pass_rate']*100:.1f}%） | 可答 {ans_pass}/{len(ans)} | 拒答 {ref_pass}/{len(ref)} | 该拒未拒 {len(halluc)}")
    print(f"报告：{out_md.relative_to(ROOT)} / {out_json.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
