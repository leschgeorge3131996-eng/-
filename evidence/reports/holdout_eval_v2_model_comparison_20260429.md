# Holdout Eval V2 Model Comparison — 2026-04-29

## Why This Run Exists

The previous `EXTENDED_EVAL_V1` comparison is useful as a regression gate, but it is not a fully neutral model benchmark. That suite has been used repeatedly while improving retrieval, citation, refusal handling, and default-model routing, so a `51 / 51` score should be read as "the current demo path is stable", not as proof that one base model is universally stronger.

This holdout set was created after that concern was raised. It uses fresh questions over smaller documents that were not the main model-selection battlefield:

- `evidence/samples/office_notice.txt`
- `evidence/samples/paper_report.md`
- `evidence/samples/research_brief.md`

The manifest is `evidence/materials/HOLDOUT_EVAL_V2_20260429.json`.

## Result Summary

| Model | Passed | Pass rate | Answerable | Refusal | Citation | Declaration | Avg latency | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `qwen3-235b-a22b-instruct-2507` | `13 / 13` | `100.0%` | `100.0%` | `100.0%` | `100.0%` | `100.0%` | `5979 ms` | Stable on fresh holdout. |
| `deepseek-v4-flash` | `13 / 13` | `100.0%` | `100.0%` | `100.0%` | `100.0%` | `100.0%` | `6067 ms` | Also stable; effectively tied with Qwen on this holdout. |
| `deepseek-v4-pro` | `4 / 13` | `30.8%` | `30.0%` | `33.3%` | `30.0%` | `30.0%` | `16070 ms` | Current provider path returned repeated HTTP 500 errors. |

## Per-Model Reports

- `evidence/reports/holdout_eval_v2_qwen3_235b_20260429.md`
- `evidence/reports/holdout_eval_v2_deepseek_v4_flash_20260429.md`
- `evidence/reports/holdout_eval_v2_deepseek_v4_pro_20260429.md`

## Interpretation

This run changes the earlier practical read:

- `deepseek-v4-flash` should **not** be dismissed. On a fresh, less-tuned holdout set, it matched Qwen on pass rate and was nearly identical on average latency.
- `qwen3-235b-a22b-instruct-2507` is still the safest judged-demo default because it has both this holdout pass and the full `EXTENDED_EVAL_V1` `51 / 51` regression pass.
- `deepseek-v4-pro` cannot be recommended on the current MaaS/provider route. The failures were runtime HTTP 500 errors, so this is a provider/integration reliability problem at least as much as a model-quality problem.

## Practical Decision

For the live competition demo, keep:

```env
MODEL_QA=qwen3-235b-a22b-instruct-2507
MODEL_SUMMARY=qwen3-235b-a22b-instruct-2507
MODEL_OUTLINE=qwen3-235b-a22b-instruct-2507
```

For future model work:

1. Keep `deepseek-v4-flash` as a serious candidate, especially for small-document and office-style workflows.
2. Do not switch the judged default until `deepseek-v4-flash` also closes the three failing `EXTENDED_EVAL_V1` cases or a broader blind set shows a clear advantage.
3. Re-test `deepseek-v4-pro` only through a more reliable provider/API path; the current route is too unstable for demo decisions.

## Combined Read With EXTENDED_EVAL_V1

| Model | Tuned regression set | Fresh holdout set | Demo suitability |
| --- | ---: | ---: | --- |
| `qwen3-235b-a22b-instruct-2507` | `51 / 51` | `13 / 13` | Best default because it wins stability across both sets. |
| `deepseek-v4-flash` | `48 / 51` | `13 / 13` | Strong candidate, but not yet safer than Qwen for the current judged route. |
| `deepseek-v4-pro` | Full run stalled / impractical | `4 / 13` with HTTP 500 failures | Not suitable on current provider path. |
