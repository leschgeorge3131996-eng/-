"""并行跑 judged_eval：把一个 manifest 拆成 K 片，K 个 judged_eval 进程同时跑，再合并。

judged_eval 是逐题串行的（~15s/题），288 题要 ~45 分钟。本 wrapper 用 --shard 把题
按 index%%K 分到 K 个独立进程并行，墙钟约缩短到 1/K。进程隔离 = 无线程安全问题。

跑法：
    .venv/Scripts/python.exe scripts/parallel_judged.py \
        --manifest evidence/materials/STRESS_EVAL_20260604.json \
        --out evidence/reports/judged_X --shards 4 [--edge --cloud-embed-model bge-m3 --rescue-sim 0.65]
合并后产出 {out}.json / {out}.md，格式与 judged_eval 一致。
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--shards", type=int, default=4)
    ap.add_argument("--judge-model", default="qwen3-235b-a22b-instruct-2507")
    ap.add_argument("--edge", action="store_true")
    ap.add_argument("--cloud-embed-model", default=None)
    ap.add_argument("--rescue-sim", type=float, default=0.50)
    ap.add_argument("--min-sim", type=float, default=0.40)
    args = ap.parse_args()

    base = [PY, "scripts/judged_eval.py", "--manifest", args.manifest,
            "--judge-model", args.judge_model, "--rescue-sim", str(args.rescue_sim),
            "--min-sim", str(args.min_sim)]
    if args.edge:
        base.append("--edge")
    if args.cloud_embed_model:
        base += ["--cloud-embed-model", args.cloud_embed_model]

    procs, shard_outs = [], []
    (ROOT / "tmp").mkdir(exist_ok=True)
    for k in range(args.shards):
        so = f"{args.out}_s{k}"
        shard_outs.append(so)
        cmd = base + ["--shard", f"{k}/{args.shards}", "--out", so]
        logf = open(ROOT / f"tmp/_pj_s{k}.log", "w", encoding="utf-8")
        procs.append(subprocess.Popen(cmd, cwd=str(ROOT), stdout=logf, stderr=subprocess.STDOUT))
    print(f"启动 {args.shards} 个分片并行（manifest={Path(args.manifest).name}, edge={args.edge}, "
          f"model={args.cloud_embed_model or ('bge-small' if args.edge else 'lexical')}, rescue_sim={args.rescue_sim}）")
    for k, p in enumerate(procs):
        p.wait()
        print(f"  分片 {k} 完成 (exit {p.returncode})")

    # 合并
    records = []
    for so in shard_outs:
        jf = ROOT / f"{so}.json"
        if jf.exists():
            try:
                records += json.loads(jf.read_text(encoding="utf-8")).get("records", [])
            except Exception as exc:  # noqa: BLE001
                print(f"  [warn] 读分片 {so} 失败: {exc}")

    total = len(records)
    passed = sum(1 for r in records if r.get("judge_pass"))
    ans = [r for r in records if r.get("kind") != "refusal"]
    ref = [r for r in records if r.get("kind") == "refusal"]
    labels: dict[str, int] = {}
    for r in records:
        labels[r.get("judge_label", "?")] = labels.get(r.get("judge_label", "?"), 0) + 1
    summary = {
        "total": total, "passed": passed,
        "pass_rate": round(passed / total, 4) if total else 0,
        "answerable_total": len(ans), "answerable_passed": sum(1 for r in ans if r.get("judge_pass")),
        "refusal_total": len(ref), "refusal_passed": sum(1 for r in ref if r.get("judge_pass")),
        "hallucinated_refusals": sum(1 for r in ref if not r.get("judge_pass")),
        "labels": labels, "judge_model": args.judge_model,
        "shards": args.shards, "manifest": args.manifest,
    }
    out_json = ROOT / f"{args.out}.json"
    out_md = ROOT / f"{args.out}.md"
    out_json.write_text(json.dumps({"summary": summary, "records": records}, ensure_ascii=False, indent=1), encoding="utf-8")
    fails = [r for r in records if not r.get("judge_pass")]
    md = [f"# 并行判分合并 · {Path(args.manifest).stem}", "",
          f"- {args.shards} 分片并行；答题 deepseek-v4-flash / 裁判 {args.judge_model}；"
          f"edge={args.edge} model={args.cloud_embed_model or ('bge-small' if args.edge else 'lexical')} rescue_sim={args.rescue_sim}",
          "", f"- 通过 **{passed}/{total} ({summary['pass_rate']*100:.1f}%)** | 可答 {summary['answerable_passed']}/{len(ans)} "
          f"| 拒答 {summary['refusal_passed']}/{len(ref)} | 标签 {labels}", "", "## 失败（人需复核）", "",
          "| case_id | 标签 | 裁判理由 |", "|---|---|---|"]
    for r in fails:
        md.append(f"| {r['case_id']} | {r.get('judge_label')} | {str(r.get('judge_reason',''))[:90]} |")
    out_md.write_text("\n".join(md), encoding="utf-8")
    print(f"\n合并完成: {passed}/{total} ({summary['pass_rate']*100:.1f}%)  标签 {labels}")
    print(f"-> {out_json.relative_to(ROOT)} / {out_md.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
