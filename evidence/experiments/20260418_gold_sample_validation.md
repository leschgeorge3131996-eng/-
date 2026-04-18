# 2026-04-18 Gold Sample Validation

## Goal

Validate the locked gold-sample candidate under the current `Wuwen Xinqiong`
runtime, compare the two QA model candidates, and refresh replay evidence that
matches the current session/document-token boundary.

## Candidate

- Document: `evidence/samples/chinese_llm_spatial_eval.pdf`
- Prompt set:
  - `这篇论文主要研究了什么问题？`
  - `作者最终的方法排名和总体准确率分别是多少？`
  - `木星有几颗卫星？`

Source manifest:

- `evidence/materials/GOLD_SAMPLE_CANDIDATE_20260418.json`

## Runtime

- Provider: `Wuwen Xinqiong`
- Base URL: `https://cloud.infini-ai.com/maas/v1/chat/completions`
- Current primary QA model: `qwen3-235b-a22b-instruct-2507`
- Validated fallback QA model: `qwen3-32b`

## Validation 1: Real In-Project Minimal Path

Verified path:

- `login -> upload -> ask -> citation -> PDF page -> PDF render`

Result:

- passed on `chinese_llm_spatial_eval.pdf`
- `ask` returned citations
- cited page fetch passed
- cited PNG render passed
- true off-topic refusal passed

## Validation 2: QA Model Comparison

Artifact:

- `evidence/reports/gold_sample_qa_compare_latest.md`

Outcome:

- `qwen3-235b-a22b-instruct-2507`: `3 / 3` passed
- `qwen3-32b`: `3 / 3` passed

Decision:

- keep `qwen3-235b-a22b-instruct-2507` as default `MODEL_QA`
- keep `qwen3-32b` as validated fallback

Reason:

- latency gap is small in this candidate set
- `235b` returned slightly richer grounding on the broad research-focus ask

## Validation 3: Replay Workflow Refresh

Updated scripts:

- `scripts/replay_sample_set.py`
- `scripts/run_real_replay.ps1`

Why:

- old replay flow did not reflect the current session/cookie + document-token
  runtime boundary

What changed:

- replay now creates a controlled-alpha session internally
- uploads are owned by that session
- task execution passes both `session_id` and `document_access_token`
- replay wrapper now supports custom manifest and name prefix

## Refreshed Evidence

Latest authoritative gold-sample replay outputs:

- `evidence/reports/gold_sample_replay_real_latest.md`
- `evidence/reports/gold_sample_replay_real_summary_latest.md`

Timestamped run from this validation:

- `evidence/reports/gold_sample_replay_real_20260418_231952.md`
- `evidence/reports/gold_sample_replay_real_summary_20260418_231952.md`

Replay result:

- `2 answered`
- `1 refused`
- `0 errors`

## Operator Notes

- For the refusal demo, keep the prompt purely off-topic.
- Do not mention in-document entities such as `作者` in the refusal prompt.
- Prefer `evidence/materials/GOLD_SAMPLE_RUNBOOK.md` for live demo execution and
  screenshot refresh.
