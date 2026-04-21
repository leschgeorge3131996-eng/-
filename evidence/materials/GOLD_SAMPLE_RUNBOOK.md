# Gold Sample Runbook

## Goal

Use the locked gold-sample candidate to run the shortest, most stable demo path:

- answerable ask with citations
- PDF evidence jump/render
- true off-topic refusal

Current candidate source:

- manifest: `evidence/materials/GOLD_SAMPLE_CANDIDATE_20260418.json`
- document: `evidence/samples/chinese_llm_spatial_eval.pdf`

## Current Prompt Set

### Answerable 1

`这篇论文主要研究了什么问题？`

Expected:

- answered
- citations present
- cited pages should include page `2` and may also include page `3`

### Answerable 2

`作者最终的方法排名和总体准确率分别是多少？`

Expected:

- answered
- answer should mention:
  - `第六`
  - `56.20%`
- citations present
- cited pages should include page `1`

### Refusal

`木星有几颗卫星？`

Expected:

- refused
- `retrieval_status=no_match`
- no citations

## Demo Path

1. Open the app and load/upload `chinese_llm_spatial_eval.pdf`
2. Ask `这篇论文主要研究了什么问题？`
3. Show the answer, citation list, and cited PDF page/render
4. Ask `作者最终的方法排名和总体准确率分别是多少？`
5. Show the concise numeric answer with its citations
6. Ask `木星有几颗卫星？`
7. Show the explicit refusal

## Pre-Demo Warmup

Before a live judging/demo slot, do this once on the actual demo machine.

### Fast path (one command)

```
.venv/Scripts/python.exe scripts/predeploy_sanity.py
```

`scripts/predeploy_sanity.py` archives `data/logs/call_logs.jsonl` (so old
`MODEL_SERVICE_ERROR` rows and long P95 tails don't leak into the stats
panel), then runs the same `3` gold prompts end-to-end through the real
`TaskService`, and writes `evidence/reports/predeploy_sanity_<timestamp>.md`.
Exit code `0` = READY, non-zero = NEEDS ATTENTION.

### Manual path (UI verification)

1. Open the app and upload the locked sample PDF
2. Run the same fixed prompt order once:
   - answerable 1
   - answerable 2
   - refusal
3. Confirm:
   - answerable results show `模型声明证据`
   - refusal shows `retrieval_status=no_match`
   - PDF preview opens on the cited page
4. Only start the live demo after the warmup run succeeds

Purpose:

- reduce cold-start latency during the judged run
- catch `candidate` evidence mode before the real demo starts
- ensure the exact machine/session already has the locked path loaded once

## Screenshot Targets

- `YYYYMMDD_gold_ask_research_focus.png`
- `YYYYMMDD_gold_pdf_render.png`
- `YYYYMMDD_gold_ask_rank_accuracy.png`
- `YYYYMMDD_gold_refusal.png`

If refreshing screenshots programmatically:

- use `node scripts/capture_gold_sample_screenshots.js`
- require answerable sidecars:
  - `YYYYMMDD_gold_ask_research_focus.json`
  - `YYYYMMDD_gold_ask_rank_accuracy.json`
- answerable sidecars must show `evidence_mode=declared`

## Report Targets

- QA comparison:
  - `evidence/reports/gold_sample_qa_compare_latest.md`
- Gold replay:
  - `evidence/reports/gold_sample_replay_real_latest.md`
  - `evidence/reports/gold_sample_replay_real_summary_latest.md`

## Operator Notes

- For the final refusal demo, do not mention document entities such as `作者`, `论文`, or in-document topics.
- If latency becomes tight in the real environment, rerun `scripts/compare_qa_models.py` before changing `MODEL_QA`.
- Prefer this runbook over the broader sample set when the goal is judging/demo stability rather than general coverage.

## Fallback Rules

If any of the following happens during a judged/demo run:

- answerable result falls back to `检索上下文`
- PDF preview does not open cleanly
- numeric answer is visibly wrong
- latency is too long to wait comfortably

Then switch immediately to the latest locked screenshot set and keep the spoken story unchanged:

- `YYYYMMDD_gold_ask_research_focus.png`
- `YYYYMMDD_gold_pdf_render.png`
- `YYYYMMDD_gold_ask_rank_accuracy.png`
- `YYYYMMDD_gold_refusal.png`

Do not improvise a new prompt or a new document mid-demo.

## G3 Recording Requirement

To close `G3`, a second operator should record:

- `3` consecutive runs
- wall-clock duration for each run
- whether warmup was done
- whether answerable results stayed `declared`
- any fallback usage

Recommended log file:

- `evidence/experiments/20260420_g3_strict_rehearsal.md`
