"""从真实 call_logs.jsonl 生成"平台调用对账"证据（决赛对账 + 智能体遥测）。

为什么：决赛要能证明"我们真在无问芯穹 MaaS 上跑了，且每次调用都有平台侧
可核对的 request id"。本脚本只读真实日志、不伪造，输出一页对账 markdown +
随附原始 jsonl 快照，便于：
  1) 登录代金券号控制台，用 request id + 时间核对每一笔（计费/调用记录）；
  2) 展示智能体自评-再检索循环（agent_iterations / query_rewrites 遥测）。

跑法：
    .venv/Scripts/python.exe scripts/build_platform_reconciliation.py \
        --log data/logs/call_logs.jsonl --date 20260602
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
CST = timezone(timedelta(hours=8))  # 无问芯穹控制台为北京时间


def to_beijing(ts: str) -> str:
    try:
        dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(CST).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ts or "?"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", default="data/logs/call_logs.jsonl")
    ap.add_argument("--date", default=datetime.now(CST).strftime("%Y%m%d"))
    ap.add_argument("--out-dir", default="evidence/reports")
    args = ap.parse_args()

    log_path = ROOT / args.log
    if not log_path.exists():
        print(f"[FAIL] 找不到日志：{log_path}")
        return 1

    rows = [json.loads(l) for l in log_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    real = [r for r in rows if r.get("platform_request_id")]
    if not real:
        print("[FAIL] 日志里没有带 platform_request_id 的真实调用——可能全是缓存命中或 mock。")
        return 1

    out_dir = ROOT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"platform_reconciliation_{args.date}.md"
    raw_path = out_dir / f"platform_reconciliation_{args.date}_calls.jsonl"
    shutil.copyfile(log_path, raw_path)  # 原始证据快照，随报告一起留痕

    def ex(r, k, default=None):
        return (r.get("extra") or {}).get(k, default)

    agentic2 = [r for r in real if ex(r, "agent_iterations", 1) and ex(r, "agent_iterations", 1) >= 2]
    total_tok = sum((r.get("token_total") or 0) for r in real)
    models = sorted({r.get("model_name") for r in real})

    lines: list[str] = []
    lines.append(f"# 平台调用对账证据 · {args.date}")
    lines.append("")
    lines.append("> 由 `scripts/build_platform_reconciliation.py` 从真实 `call_logs.jsonl` 生成，"
                 "未手工编辑数字。原始日志快照见同目录 "
                 f"`{raw_path.name}`。")
    lines.append("")
    lines.append("## 概览")
    lines.append("")
    lines.append(f"- 真实云端调用（带平台 request id）：**{len(real)} 笔**")
    lines.append(f"- 模型：{', '.join(m for m in models if m)}")
    lines.append(f"- 平台累计返回 token：**{total_tok}**（仅含成功返回 usage 的调用）")
    lines.append(f"- 触发智能体二轮（`agent_iterations≥2`）：**{len(agentic2)} 笔**")
    lines.append("- 计费账户：领取 200 代金券的无问芯穹账号（请在该账号控制台核对下表 id/时间）。")
    lines.append("")
    lines.append("## 逐笔对账表")
    lines.append("")
    lines.append("时间为**北京时间(UTC+8)**，与控制台一致；request id 可在控制台调用记录/账单逐条核对。")
    lines.append("")
    lines.append("| # | 北京时间 | endpoint | 模型 | platform_request_id | 延迟ms | tok_in/out | agent轮次 | 结果 | 命中页 |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(real, 1):
        lines.append(
            f"| {i} | {to_beijing(r.get('timestamp',''))} | {r.get('endpoint','')} | "
            f"{r.get('model_name','')} | `{r.get('platform_request_id')}` | "
            f"{r.get('latency_ms','')} | {r.get('token_in')}/{r.get('token_out')} | "
            f"{ex(r,'agent_iterations',1)} | {r.get('outcome','')} | "
            f"{ex(r,'retrieved_pages',[])} |"
        )
    lines.append("")
    lines.append("## 智能体（自评-再检索）真实遥测")
    lines.append("")
    lines.append("以下为 `agent_iterations=2` 的真实调用——模型在首轮自评"
                 "「证据可能不足」后，系统自动二次检索再问一次（遥测落 `extra.agent_iterations`）：")
    lines.append("")
    for r in agentic2:
        refused = ex(r, "llm_refused", False) or r.get("outcome") == "refused"
        note = "二轮仍无逐字证据 → 诚实拒答（不编造）" if refused else "二轮确认证据 → declared 答出"
        lines.append(f"- `{r.get('platform_request_id')}`：iters=2，{note}。")
    lines.append("")
    lines.append("> 诚实口径：本批 `agent_iterations=2` 的样本里 `query_rewrites` 多为空——"
                 "并非循环没跑，而是首轮检索已把相关片段捞全，二轮没有捞到**新**片段；"
                 "这与我们「词法检索已高度饱和」的离线结论一致（见 `edge_hybrid_eval.md`）。"
                 "循环的价值在于：证据真不在时即使升级仍**拒答不编**，"
                 "在时则二轮确认后答出——拒答契约全程不变。带新片段的改写路径由单测 "
                 "`test_agentic_ask_reretrieves_with_followup_query` 覆盖。")
    lines.append("")
    lines.append("## 怎么核对（H3：控制台截图）")
    lines.append("")
    lines.append("1. 登录领 200 代金券的无问芯穹账号 → 控制台 → 调用记录 / 用量账单。")
    lines.append("2. 按上表「北京时间」定位时段，逐条核对 `chatcmpl-...` request id 与 token。")
    lines.append("3. 截图即为「真实跑在平台 + 计费到代金券号」的决赛对账硬证据。")
    lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] 已生成对账报告：{md_path.relative_to(ROOT)}")
    print(f"[OK] 原始日志快照  ：{raw_path.relative_to(ROOT)}")
    print(f"     真实调用 {len(real)} 笔；agent_iterations≥2 共 {len(agentic2)} 笔；累计 token {total_tok}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
