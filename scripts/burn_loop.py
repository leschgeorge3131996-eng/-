"""持续烧券 + 找短板的长循环（设计跑 ~2 天）。

每轮：强模型现造一大批新题 -> 真实链路作答 + 源接地判分 -> 把失败累计进
cumulative 报告。复用现成的 generate_eval_questions.py + judged_eval.py（subprocess，
不耦合内部实现），所以稳健、可续跑。

停止：到 --hours 截止，或出现 tmp/STOP_BURN 文件即优雅退出（当前 batch 跑完）。
监控：evidence/reports/burn_campaign_cumulative.json 每轮更新（题量 / 估算调用数 /
失败标签分布 / 按文档失败数 / 样例）。每批原始件落 tmp/burn/（gitignore）。

跑法（后台）：
    .venv/Scripts/python.exe -u scripts/burn_loop.py --hours 47 --answerable 20 --refusal 10
环境变量同名可覆盖：BURN_HOURS / BURN_ANS / BURN_REF / BURN_SLEEP
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
BURN_DIR = ROOT / "tmp" / "burn"
STOP = ROOT / "tmp" / "STOP_BURN"
CUM = ROOT / "evidence" / "reports" / "burn_campaign_cumulative.json"

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=float, default=47.0)
    ap.add_argument("--answerable", type=int, default=20)
    ap.add_argument("--refusal", type=int, default=10)
    ap.add_argument("--sleep", type=int, default=15)
    args = ap.parse_args()

    BURN_DIR.mkdir(parents=True, exist_ok=True)
    CUM.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.time() + args.hours * 3600

    cum = {
        "started": time.strftime("%Y-%m-%d %H:%M:%S"),
        "batches": 0, "questions": 0, "est_calls": 0,
        "pass": 0, "fail": 0, "labels": {}, "by_doc_fail": {}, "fail_samples": [],
    }
    if CUM.exists():
        try:
            cum = json.loads(CUM.read_text(encoding="utf-8"))  # resume across restarts
        except Exception:
            pass

    batch = cum.get("batches", 0)
    print(f"[burn] start; deadline in {args.hours}h; batch size ~{(args.answerable + args.refusal) * 16}", flush=True)

    while time.time() < deadline:
        if STOP.exists():
            print("[burn] STOP_BURN present -> graceful halt.", flush=True)
            break
        batch += 1
        stamp = f"burn_b{batch:04d}"
        man = BURN_DIR / f"{stamp}.json"
        rep = BURN_DIR / stamp  # judged_eval -> rep.md / rep.json

        print(f"[burn] batch {batch}: generating...", flush=True)
        subprocess.run(
            [PY, "scripts/generate_eval_questions.py", "--out", str(man),
             "--answerable", str(args.answerable), "--refusal", str(args.refusal)],
            cwd=str(ROOT),
        )
        if not man.exists():
            print("[burn] generation produced no manifest; backoff 60s.", flush=True)
            time.sleep(60)
            continue

        print(f"[burn] batch {batch}: judging...", flush=True)
        subprocess.run(
            [PY, "scripts/judged_eval.py", "--manifest", str(man), "--out", str(rep)],
            cwd=str(ROOT),
        )

        jf = Path(str(rep) + ".json")
        if jf.exists():
            try:
                d = json.loads(jf.read_text(encoding="utf-8"))
            except Exception:
                d = {}
            recs = d.get("records", [])
            passed = sum(1 for r in recs if r.get("judge_pass"))
            cum["batches"] = batch
            cum["questions"] += len(recs)
            cum["est_calls"] += len(recs) * 2  # ~1 ask + ~1 judge per question
            cum["pass"] += passed
            cum["fail"] += len(recs) - passed
            for r in recs:
                if not r.get("judge_pass"):
                    lab = r.get("judge_label", "?")
                    cum["labels"][lab] = cum["labels"].get(lab, 0) + 1
                    doc = r["case_id"].split(":")[0]
                    cum["by_doc_fail"][doc] = cum["by_doc_fail"].get(doc, 0) + 1
                    if len(cum["fail_samples"]) < 300:
                        cum["fail_samples"].append({
                            "batch": batch, "case_id": r["case_id"], "label": r.get("judge_label"),
                            "reason": str(r.get("judge_reason"))[:140], "answer": str(r.get("answer"))[:140],
                        })
            cum["updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
            CUM.write_text(json.dumps(cum, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"[burn] batch {batch} done | cum: {cum['questions']} Q, ~{cum['est_calls']} calls, "
                  f"pass {cum['pass']} fail {cum['fail']} | labels {cum['labels']}", flush=True)
        else:
            print(f"[burn] batch {batch}: judged report missing; continuing.", flush=True)

        time.sleep(args.sleep)

    print(f"[burn] ENDED. batches={batch} questions={cum.get('questions')} est_calls={cum.get('est_calls')}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
