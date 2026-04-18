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

## Screenshot Targets

- `YYYYMMDD_gold_ask_research_focus.png`
- `YYYYMMDD_gold_pdf_render.png`
- `YYYYMMDD_gold_ask_rank_accuracy.png`
- `YYYYMMDD_gold_refusal.png`

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
