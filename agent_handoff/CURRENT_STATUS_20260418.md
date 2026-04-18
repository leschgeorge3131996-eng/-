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

## Current Meaning

- Wuwen Xinqiong integration itself is no longer the blocker
- The project has moved from “external API validation” to “real in-project flow validation”
- The main demo chain `ask -> citation -> PDF` has now been verified in-project under the current Wuwen Xinqiong `.env`

## Recommended Next Step

1. Lock one gold-sample candidate PDF and final candidate prompts:
   - `2 answerable`
   - `1 refusal` that is truly off-topic
2. Run the same ask/refusal path again with `MODEL_QA=qwen3-32b`
3. Compare:
   - answer quality
   - citation stability
   - refusal precision
   - latency
4. Then decide whether `MODEL_QA` should stay on `qwen3-235b-a22b-instruct-2507` or fall back to `qwen3-32b`
5. Refresh real-only evidence outputs and screenshots after the gold sample is locked
