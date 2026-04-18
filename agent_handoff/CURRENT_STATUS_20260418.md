# Current Status 2026-04-18

## Execution Baseline

- Active baseline: `agent_handoff/COMPETITION_PLAN_V2.md`
- Future optimization work should follow that plan unless explicitly replaced

## Wuwen Xinqiong Integration

- Default interface verified:
  - `https://cloud.infini-ai.com/maas/v1/chat/completions`
- Current primary model decision:
  - primary: `qwen3-235b-a22b-instruct-2507`
  - fallback: `qwen3-32b`
- External minimal verification completed for both models
- Project-local `.env` is now reading:
  - `MODEL_PROVIDER=infinigence_ai`
  - `USE_MOCK_MODEL=false`
  - `WUQIONG_BASE_URL=https://cloud.infini-ai.com/maas/v1`
  - `MODEL_QA/MODEL_SUMMARY/MODEL_OUTLINE=qwen3-235b-a22b-instruct-2507`

## Project-Internal Verification

- `summary` real call through Wuwen Xinqiong: passed
- `ask` real call through Wuwen Xinqiong: passed
- Returned model during internal verification:
  - `qwen3-235b-a22b-instruct-2507`

## Code Fix Applied

- File changed:
  - `backend/app/services/model_client.py`
- Change:
  - fixed the `ask` prompt template JSON example by escaping inner braces correctly
- Reason:
  - `call_model(task_type='ask', ...)` previously crashed locally with a `ValueError` before any network call
- Result after fix:
  - internal `ask` now returns structured JSON with:
    - `answer`
    - `used_chunk_ids`
    - `evidence_quotes`

## Verification

- Backend tests rerun after the fix:
  - `54 passed`

## Real In-Project Minimal Path Validation (`2026-04-18`)

- Environment note:
  - current active `.env` is the new `Wuwen Xinqiong` config
  - old replay reports using prior providers should be treated as historical only
- Validation sample:
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
- Answerable path:
  - `login -> upload -> ask -> citation -> PDF page -> PDF render`: passed
  - returned model: `qwen3-235b-a22b-instruct-2507`
  - `ask` latency: about `6686 ms`
  - retrieval status: `matched`
  - citation count: `2`
  - cited page fetch: passed
  - cited page render (`image/png`): passed
- True off-topic refusal check:
  - question: `木星有几颗卫星？`
  - result: refused correctly
  - retrieval status: `no_match`
  - latency: about `38 ms`
- Caution:
  - a semi-related "refusal" prompt that still mentions document entities (for example `作者`) may retrieve matching chunks and produce an answer
  - the final refusal demo prompt should therefore be purely off-topic
- Debugging note:
  - one earlier local false negative came from PowerShell -> inline Python encoding turning Chinese prompt literals into `?`
  - that was a validation harness issue, not a project retrieval bug

## Gold Sample Candidate Lock (`2026-04-18`)

- Candidate PDF:
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
- Candidate prompt set:
  - answerable 1: `这篇论文主要研究了什么问题？`
  - answerable 2: `作者最终的方法排名和总体准确率分别是多少？`
  - refusal: `木星有几颗卫星？`
- Candidate manifest saved at:
  - `evidence/materials/GOLD_SAMPLE_CANDIDATE_20260418.json`

## QA Model Comparison (`2026-04-18`)

- Reusable comparison script added:
  - `scripts/compare_qa_models.py`
- Latest report outputs:
  - `evidence/reports/gold_sample_qa_compare_latest.md`
  - `evidence/reports/gold_sample_qa_compare_latest.json`
- Compared models:
  - `qwen3-235b-a22b-instruct-2507`
  - `qwen3-32b`
- Result:
  - both models passed `2 answerable + 1 refusal`
  - both answerable prompts returned citations and passed page/render validation
  - both models refused the off-topic prompt correctly
- Latency summary:
  - `qwen3-235b-a22b-instruct-2507`: average about `4896 ms`
  - `qwen3-32b`: average about `4396 ms`
- Quality/citation observation:
  - `qwen3-235b-a22b-instruct-2507` returned slightly richer grounding on the broader research-focus question
  - `qwen3-32b` was slightly faster, but typically returned fewer citations/evidence quotes
- Current decision:
  - keep `qwen3-235b-a22b-instruct-2507` as the primary `MODEL_QA`
  - keep `qwen3-32b` as the validated fallback option

## Current Meaning

- Wuwen Xinqiong integration itself is no longer the blocker
- The project has moved from “external API validation” to “real in-project flow validation”
- The main demo chain `ask -> citation -> PDF` has now been verified in-project under the current Wuwen Xinqiong `.env`
- A Chinese gold-sample candidate and candidate question set are now locked for the current stage
- The current `MODEL_QA` decision can remain on `qwen3-235b-a22b-instruct-2507` without blocking `G2`

## Recommended Next Step

1. Refresh real-only evidence around the locked candidate set:
   - answerable ask screenshot with citations
   - cited PDF render screenshot
   - refusal screenshot
2. Decide whether to regenerate replay/evidence artifacts using the locked candidate set instead of the older broad sample set
3. If deployment/demo latency becomes a practical issue, rerun the same compare script before switching `MODEL_QA` to `qwen3-32b`
4. Start turning the locked candidate set into paper/PPT/video/poster source material after screenshot evidence is refreshed
