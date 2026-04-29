# V6 Contract Patch - Qwen3 235B vs DeepSeek V4 Flash

Date: 2026-04-30

## What changed

The ask prompt and evidence-retry prompt were tightened before this rerun:

- Answer language must follow the user's question language.
- Explicit missing fields are separated from true out-of-scope refusal.
- Unresolved conflicts should be answered as evidence-backed uncertainty, not generic refusal.

Files changed:

- `backend/app/services/model_client.py`
- `backend/app/services/task_service.py`
- `backend/tests/test_services.py`

## Test command

Both models were rerun on:

`evidence/materials/HOLDOUT_EVAL_V6_EXTREME_FULL_20260430.json`

## Result

| Model | Strict Pass | Avg Latency | Refusal Precision | Citation Accuracy | Declaration Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| `qwen3-235b-a22b-instruct-2507` | 56 / 72 | 5872 ms | 92.3% | 74.6% | 74.6% |
| `deepseek-v4-flash` | 71 / 72 | 5952 ms | 100.0% | 98.3% | 98.3% |

DeepSeek V4 Flash now leads by `+15` strict cases after the contract patch. The latency gap is only `80 ms`, effectively negligible for the judged demo path.

## Interpretation

The contract patch helped the two models differently:

- Qwen became much better at refusal precision, but it became more likely to fall back to candidate evidence without declared quotes/citations.
- Flash handled the stricter contract very well: it retained high citation/declaration quality and reached perfect refusal precision.

Flash's only remaining failure was:

- `nested_exception_policy_v6:marketing_exception`
  - The answer was semantically reasonable: the document says no exception is created for marketing surveys.
  - It was marked failed because the model returned it through the refusal path without citations, instead of as an evidence-backed boundary answer.

## Sanity gate

`deepseek-v4-flash` was also tested on the predeploy sanity path by setting `MODEL_QA=deepseek-v4-flash` for that run.

Result:

- Gold cases: `3 / 3`
- Runtime gates: `11 / 11`
- Status: `READY`
- Report: `evidence/reports/predeploy_sanity_20260430_010552.md`

## Decision

DeepSeek V4 Flash has now met the switch gate that was proposed after V6:

- Leads Qwen by more than `+3` strict cases on frozen V6.
- Passes gold/predeploy sanity.
- Maintains stronger citation/declaration behavior.
- Maintains perfect refusal precision on this run.

Recommendation:

- Use `deepseek-v4-flash` as the QA default for rehearsal.
- Keep `qwen3-235b-a22b-instruct-2507` as rollback fallback.
- Leave summary and outline on Qwen for now to minimize blast radius.

