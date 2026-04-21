# Predeploy Sanity Report — 20260421_225141

**Status:** READY (3/3 gold cases passed)

## Log hygiene

- Live `call_logs.jsonl` was already empty; no archive needed

## Gold cases

| Case | Kind | Pass | Outcome | Retrieval | Evidence | Pages | Latency | Note |
| --- | --- | --- | --- | --- | --- | --- | ---: | --- |
| answerable_research_focus | answerable | PASS | answered | matched | declared | [1, 2] | 9036 | - |
| answerable_rank_accuracy | answerable | PASS | answered | matched | declared | [1] | 6086 | - |
| refusal_jupiter_moons | refusal | PASS | refused | no_match | none | [] | 8 | - |

## Per-case answer snippets

### answerable_research_focus
- **Passed:** True
- **Answer snippet:** 这篇论文主要研究了大语言模型对空间语义的理解程度以及在具体任务中的优劣，基于第四届中文空间语义理解评测任务（SpaCE2024）进行实验分析，探讨大模型在空间语义理解方面的能力边界。

### answerable_rank_accuracy
- **Passed:** True
- **Answer snippet:** 作者最终的方法排名第六，总体准确率为56.20%。

### refusal_jupiter_moons
- **Passed:** True
- **Answer snippet:** 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。

## What to do if status is NEEDS ATTENTION

1. Check backend env: `WUQIONG_BASE_URL` / `WUQIONG_API_KEY` / `MODEL_QA`.
2. Re-run this script after fixing env vars.
3. If still failing: fall back to the locked screenshot set (`evidence/screenshots/20260419_gold_*.png`) and use the spoken story unchanged — see `DEFENSE_DEMO_RISK_CHECKLIST.md`.
