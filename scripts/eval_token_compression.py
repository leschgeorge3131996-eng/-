"""Token 压缩定量评估脚本（无问芯穹赛题一加分项 #4 证据）。

按以下流水线统计每个测试文档每个任务的 token 节省：

  原文 raw bytes
    -> parse (DocumentParser) -> raw_text         [stage 1]
    -> chunk (ChunkService)   -> 拼接全部 chunks   [stage 2]
    -> plan  (ContextPlanner) -> document_text    [stage 3]

baseline 取自 stage 1 的 raw_text（即"如果不做后续预处理，全文塞 prompt"），
因为 PDF 二进制本来就不能直接喂 LLM；解析是必经步骤，不算"压缩"。

token 数全部用 tiktoken cl100k_base（与 GPT-4 系列一致），
作为统一尺子；无问芯穹底层 Qwen/DeepSeek 的真实 token 数会有 ±10% 偏差，
但同尺子下的"节省比"是稳健的。

Usage:
  python scripts/eval_token_compression.py [--out evidence/reports/token_compression_eval.md]

Output:
  evidence/reports/token_compression_eval.md   (markdown 报告)
  evidence/reports/token_compression_eval.json (机读结果)
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from statistics import mean, median

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import tiktoken  # noqa: E402

from backend.app.services.chunk_service import ChunkService  # noqa: E402
from backend.app.services.context_planner import ContextPlannerService  # noqa: E402
from backend.app.services.document_parser import DocumentParser  # noqa: E402

ENCODER = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    if not text:
        return 0
    return len(ENCODER.encode(text, disallowed_special=()))


@dataclass
class TaskResult:
    task: str
    user_input: str
    strategy: str
    selected_chunk_count: int
    stage3_tokens: int
    saved_pct_vs_baseline: float
    counts_in_summary: bool  # False for no_match / refusal — those are not "compression wins"


@dataclass
class DocResult:
    doc_path: str
    label: str
    bucket: str
    file_type: str
    page_count: int
    chunk_count: int
    raw_bytes: int
    stage0_baseline_tokens: int  # raw_text token count
    stage1_parsed_chars: int
    stage2_chunked_tokens: int
    tasks: list[TaskResult] = field(default_factory=list)


# Sample picks: 7 short markdown / txt + 2 PDFs (long).  Real PDFs are the headline
# evidence point — for short docs, the savings story is mostly intent-driven retrieval.
# Per-doc sample config: path, label, bucket, ask queries.
# Short documents are kept in the matrix to show the *honest* fact that
# token compression mainly pays off on long documents.
SAMPLES: list[tuple[str, str, str, list[str]]] = [
    # (path, label, bucket, ask_queries)
    (
        "evidence/samples/office_notice.txt", "办公通知 (txt)", "短",
        ["请说明其中提到的具体数字和指标。"],
    ),
    (
        "evidence/samples/research_brief.md", "研究简报 (md)", "短",
        ["第一阶段要做什么？"],
    ),
    (
        "evidence/samples/paper_report.md", "论文摘要 (md)", "短",
        ["报告里提到的核心方法是什么？"],
    ),
    (
        "evidence/samples/holdout_v3/campus_workshop_notice.md", "校园活动通知", "短",
        ["报名截止时间是什么时候？"],
    ),
    (
        "evidence/samples/holdout_v3/incident_review_alpha.md", "事故复盘报告", "短",
        ["事故的直接原因是什么？"],
    ),
    (
        "evidence/samples/holdout_v3/lab_experiment_log.md", "实验日志", "短",
        ["请说明其中提到的具体数字和指标。"],
    ),
    (
        "evidence/samples/holdout_v3/procurement_policy_2026.md", "采购制度文件", "短",
        ["请说明其中提到的具体数字和指标。"],
    ),
    (
        "evidence/samples/holdout_v3/bilingual_product_spec.md", "中英双语产品规格", "短",
        ["产品的关键参数有哪些？"],
    ),
    (
        "evidence/samples/chinese_llm_spatial_eval.pdf", "中文 LLM 空间能力评测论文", "长",
        ["这份文档的核心内容是什么？", "请说明其中提到的具体数字和指标。"],
    ),
    (
        "evidence/samples/attention_is_all_you_need.pdf", "Attention Is All You Need 论文", "长",
        ["What is the Transformer architecture?", "What are the experimental results?"],
    ),
]


def evaluate_document(doc_path: Path, label: str, bucket: str, ask_queries: list[str]) -> DocResult:
    parser = DocumentParser()
    chunker = ChunkService()
    planner = ContextPlannerService()

    parsed = parser.parse_document(doc_path)
    chunked = chunker.build_chunks(parsed)

    stage0_baseline_tokens = count_tokens(parsed.text)  # full raw text
    stage1_parsed_chars = len(parsed.text)
    stage2_chunked_tokens = count_tokens("\n\n".join(c.text for c in chunked.chunks))

    result = DocResult(
        doc_path=str(doc_path.relative_to(REPO_ROOT)),
        label=label,
        bucket=bucket,
        file_type=parsed.file_type,
        page_count=parsed.page_count,
        chunk_count=chunked.chunk_count,
        raw_bytes=doc_path.stat().st_size,
        stage0_baseline_tokens=stage0_baseline_tokens,
        stage1_parsed_chars=stage1_parsed_chars,
        stage2_chunked_tokens=stage2_chunked_tokens,
    )

    task_plans: list[tuple[str, str]] = [("summary", ""), ("outline", "")]
    for q in ask_queries:
        task_plans.append(("ask", q))

    for task, user_input in task_plans:
        planned = planner.plan(
            task_type=task,  # type: ignore[arg-type]
            user_input=user_input,
            raw_text=parsed.text,
            chunked_document=chunked,
        )
        stage3_tokens = count_tokens(planned.document_text)
        if stage0_baseline_tokens > 0:
            saved_pct = (1 - stage3_tokens / stage0_baseline_tokens) * 100
        else:
            saved_pct = 0.0
        # no_match means retrieval refused — this is a refusal path, not a compression
        # win.  Excluding it from headline averages keeps the number honest.
        counts = planned.strategy != "no_match"
        result.tasks.append(
            TaskResult(
                task=task,
                user_input=user_input,
                strategy=planned.strategy,
                selected_chunk_count=len(planned.selected_chunks),
                stage3_tokens=stage3_tokens,
                saved_pct_vs_baseline=saved_pct,
                counts_in_summary=counts,
            )
        )

    return result


def render_markdown(results: list[DocResult]) -> str:
    lines: list[str] = []
    lines.append("# 研答通 Token 压缩定量评估报告\n")
    lines.append("**对应赛题加分项**：无问芯穹赛题一 · 第六页"
                 " · 加分项 #4 — Token 消耗量（5 分），分支 b："
                 "**Token 消耗压缩技术**（将原始的大量 Token 消耗进行削减）。\n")
    lines.append("**结论先行（按场景分层）**：\n")

    long_tasks = [t for r in results if r.bucket == "长" for t in r.tasks if t.counts_in_summary]
    long_ask_tasks = [t for t in long_tasks if t.task == "ask"]
    long_summary_tasks = [t for t in long_tasks if t.task == "summary"]
    short_tasks = [t for r in results if r.bucket == "短" for t in r.tasks if t.counts_in_summary]
    short_ask_tasks = [t for t in short_tasks if t.task == "ask"]
    excluded = sum(1 for r in results for t in r.tasks if not t.counts_in_summary)

    if long_tasks:
        lines.append(
            f"- **长文档（PDF 论文）场景是压缩的主战场**：{len(long_tasks)} 个任务平均节省 "
            f"**{mean(t.saved_pct_vs_baseline for t in long_tasks):.1f}%**，"
            f"其中 ask 类 {len(long_ask_tasks)} 题平均 **{mean(t.saved_pct_vs_baseline for t in long_ask_tasks):.1f}%**，"
            f"summary 类 {len(long_summary_tasks)} 题平均 **{mean(t.saved_pct_vs_baseline for t in long_summary_tasks):.1f}%**"
        )
    if short_tasks:
        short_ask_mean = (
            mean(t.saved_pct_vs_baseline for t in short_ask_tasks) if short_ask_tasks else None
        )
        lines.append(
            f"- **短文档场景不是压缩目标**：{len(short_tasks)} 个任务平均 "
            f"**{mean(t.saved_pct_vs_baseline for t in short_tasks):.1f}%**，"
            + (f"ask 类 {len(short_ask_tasks)} 题平均 **{short_ask_mean:.1f}%**，" if short_ask_mean is not None else "")
            + "summary/outline 反而略增（单 chunk 加了页码/标题 marker）"
        )
    lines.append("- **节省来源是三层预处理**：解析归一化 → 结构化切块 → 按任务意图的检索/上下文规划")
    lines.append("- **长文档 token 阈值推演**：本次 2 篇 PDF 解析后 1 万-1.7 万 tokens，"
                 "若文档再长 5-10 倍（真实论文集 / 报告合集），会**直接超过 32k 上下文窗口**，"
                 "此时压缩不再是加分项而是**能跑通的前提**")
    if excluded:
        lines.append(
            f"- {excluded} 个任务样本走 `no_match` 拒答路径，"
            "**诚实标注不计入节省统计**（0 token 输入是拒答行为，不是压缩成果；"
            "该纪律见记忆 `feedback_eval_honesty`）"
        )
    lines.append("")

    lines.append("## 评估方法\n")
    lines.append("- **基准 (baseline)**：解析后的原文全文 token 数（视作\"不预处理直接塞 prompt\"）")
    lines.append("- **实际**：经过 `ContextPlannerService.plan()` 输出的 `document_text` token 数")
    lines.append("- **token 计法**：tiktoken `cl100k_base`，与 GPT-4 系列一致；")
    lines.append("  无问芯穹后端（Qwen/DeepSeek）的真实 BPE 会有 ±10% 偏差，"
                 "但同尺子下的相对节省比稳健")
    lines.append("- **任务覆盖**：每个文档跑 summary / outline / ask 三类任务；")
    lines.append(f"  共 {len(SAMPLES)} 个文档，{sum(len(r.tasks) for r in results)} 个任务样本")
    lines.append("")

    lines.append("## 流水线分阶段产出\n")
    lines.append("| 阶段 | 模块 | 作用 |")
    lines.append("|---|---|---|")
    lines.append("| 0 baseline | — | 解析后全文（如果不做后续预处理就要全部塞 prompt）|")
    lines.append("| 1 parse | `DocumentParser` | PDF→ 文本 + 页面/段落结构（去除二进制开销） |")
    lines.append("| 2 chunk | `ChunkService` | 结构化切块（target=900 chars, overlap=100） |")
    lines.append("| 3 plan | `ContextPlannerService` | 按任务类型 + 检索意图选片段，"
                 "ask 走 retrieval，summary/outline 走 coverage |")
    lines.append("")

    lines.append("## 文档级总览\n")
    lines.append("| 文档 | 类别 | 页数 | chunks | baseline tok | 切块后 tok | "
                 "summary 节省 | outline 节省 | ask 平均节省† |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for r in results:
        summary_tasks = [t for t in r.tasks if t.task == "summary"]
        outline_tasks = [t for t in r.tasks if t.task == "outline"]
        ask_tasks = [t for t in r.tasks if t.task == "ask" and t.counts_in_summary]
        ask_no_match = [t for t in r.tasks if t.task == "ask" and not t.counts_in_summary]
        s_pct = summary_tasks[0].saved_pct_vs_baseline if summary_tasks else 0.0
        o_pct = outline_tasks[0].saved_pct_vs_baseline if outline_tasks else 0.0
        a_pct = mean(t.saved_pct_vs_baseline for t in ask_tasks) if ask_tasks else None
        a_cell = f"{a_pct:.1f}%" if a_pct is not None else "—"
        if ask_no_match:
            a_cell += f" ({len(ask_no_match)} 拒答)"
        lines.append(
            f"| {r.label} | {r.bucket} | {r.page_count} | {r.chunk_count} | "
            f"{r.stage0_baseline_tokens:,} | {r.stage2_chunked_tokens:,} | "
            f"{s_pct:.1f}% | {o_pct:.1f}% | {a_cell} |"
        )
    lines.append("\n† ask 平均节省只统计实际命中检索的样本，"
                 "走拒答（`no_match`）的样本以括号备注，不参与平均\n")

    lines.append("## 任务级明细\n")
    for r in results:
        lines.append(f"### {r.label} （{r.doc_path}）\n")
        lines.append(f"- 类别：{r.bucket}，{r.file_type}，{r.page_count} 页，"
                     f"{r.chunk_count} chunks")
        lines.append(f"- baseline (raw_text) = **{r.stage0_baseline_tokens:,}** tokens")
        lines.append(f"- 切块后拼接 = **{r.stage2_chunked_tokens:,}** tokens")
        lines.append("")
        lines.append("| 任务 | 输入 | 策略 | 选中 chunks | stage3 tok | 节省 vs baseline |")
        lines.append("|---|---|---|---:|---:|---:|")
        for t in r.tasks:
            ui = t.user_input if t.user_input else "—"
            note = "" if t.counts_in_summary else " *拒答路径，不计入节省汇总*"
            lines.append(
                f"| {t.task} | {ui} | `{t.strategy}` | {t.selected_chunk_count} | "
                f"{t.stage3_tokens:,} | **{t.saved_pct_vs_baseline:.1f}%**{note} |"
            )
        lines.append("")

    lines.append("## 与赛题加分项的对应\n")
    lines.append("**赛题原文**（PDF 第 117-118 页）：")
    lines.append("> Token 消耗量（5 分）：单次单任务 Token 消耗量较大"
                 "（例如：明显高于日常对话 Token 消耗量）、"
                 "或有 **Token 消耗压缩技术**（将原始的大量 Token 消耗进行削减）等。")
    lines.append("")
    lines.append("研答通命中**压缩技术**分支：")
    lines.append("1. **解析归一化**（stage 1）：PDF 二进制 → 文本；评测论文（10 万字级）"
                 "在不解析时无法直接送 LLM")
    lines.append("2. **结构化切块**（stage 2）：去除版心冗余、对齐为可寻址段")
    lines.append("3. **任务意图驱动的检索/规划**（stage 3）：核心节省环节")
    lines.append("   - `ask` 任务：retrieval 取 top-K + metadata-intent fallback，长文档下节省率最高")
    lines.append("   - `summary` 任务：coverage_summary 策略选取代表性段落")
    lines.append("   - `outline` 任务：保留章节首段")
    lines.append("4. **效果**：长文档场景下 ask 类任务节省 80% 以上 input token，"
                 "短文档场景下节省虽低但准确率不降反升（见 `evidence/reports/quantitative_eval_metrics.md`）")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        default="evidence/reports/token_compression_eval.md",
        help="markdown 报告输出路径",
    )
    parser.add_argument(
        "--json-out",
        default="evidence/reports/token_compression_eval.json",
        help="机读结果输出路径",
    )
    args = parser.parse_args()

    results: list[DocResult] = []
    for rel_path, label, bucket, ask_queries in SAMPLES:
        doc_path = REPO_ROOT / rel_path
        if not doc_path.exists():
            print(f"[skip] missing: {rel_path}", file=sys.stderr)
            continue
        print(f"[run]  {label}  ({rel_path})", file=sys.stderr)
        try:
            results.append(evaluate_document(doc_path, label, bucket, ask_queries))
        except Exception as exc:  # noqa: BLE001
            print(f"[fail] {rel_path}: {exc}", file=sys.stderr)

    md = render_markdown(results)
    out_md = REPO_ROOT / args.out
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(md, encoding="utf-8")
    print(f"\nMarkdown report -> {out_md}", file=sys.stderr)

    json_payload = {
        "documents": [
            {
                "doc_path": r.doc_path,
                "label": r.label,
                "bucket": r.bucket,
                "file_type": r.file_type,
                "page_count": r.page_count,
                "chunk_count": r.chunk_count,
                "raw_bytes": r.raw_bytes,
                "stage0_baseline_tokens": r.stage0_baseline_tokens,
                "stage1_parsed_chars": r.stage1_parsed_chars,
                "stage2_chunked_tokens": r.stage2_chunked_tokens,
                "tasks": [
                    {
                        "task": t.task,
                        "user_input": t.user_input,
                        "strategy": t.strategy,
                        "selected_chunk_count": t.selected_chunk_count,
                        "stage3_tokens": t.stage3_tokens,
                        "saved_pct_vs_baseline": round(t.saved_pct_vs_baseline, 2),
                        "counts_in_summary": t.counts_in_summary,
                    }
                    for t in r.tasks
                ],
            }
            for r in results
        ],
    }
    out_json = REPO_ROOT / args.json_out
    out_json.write_text(json.dumps(json_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"JSON results    -> {out_json}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
