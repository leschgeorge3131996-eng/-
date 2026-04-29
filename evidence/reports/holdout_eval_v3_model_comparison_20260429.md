# Holdout Eval V3 Model Comparison — 2026-04-29

## Purpose

This run expands the model comparison from a small holdout to a larger, harder, pre-registered set.

Compared with `HOLDOUT_EVAL_V2_20260429`, V3 adds:

- `5` new synthetic-but-realistic documents under `evidence/samples/holdout_v3/`
- `75` total QA cases
- `24` reasoning cases, including arithmetic, cross-section comparison, negative-boundary questions, and simple policy decisions
- bilingual coverage through `bilingual_product_spec.md`

The compared models are:

- `qwen3-235b-a22b-instruct-2507`
- `deepseek-v4-flash`

`deepseek-v4-pro` is excluded from this round because previous runs showed provider-path HTTP 500 / stall behavior rather than stable model-quality behavior.

## Strict Automated Score

The strict scorer is intentionally simple and pre-registered:

- answerable cases require expected page hit, `evidence_mode=declared`, and at least one expected string match
- refusal cases require `retrieval_status=no_match` or `outcome=refused`
- no post-run changes were made to the manifest or scoring script

| Model | Passed | Pass rate | Answerable | Refusal | Citation | Declaration | Avg latency |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `qwen3-235b-a22b-instruct-2507` | `73 / 75` | `97.3%` | `98.6%` | `80.0%` | `100.0%` | `100.0%` | `5290 ms` |
| `deepseek-v4-flash` | `70 / 75` | `93.3%` | `94.3%` | `80.0%` | `100.0%` | `100.0%` | `5445 ms` |

Raw strict-score read: Qwen leads by `3` cases and is slightly faster on average (`155 ms`).

## Failure Triage

### Qwen Failures

| Case | Failure type | Observed behavior |
| --- | --- | --- |
| `campus_workshop_v3:campus_meal_refusal` | `refusal_escape` | Answered "本通知没有提供餐饮补贴信息" instead of using the formal refusal branch. Content is safe, but it fails the strict refusal contract. |
| `campus_workshop_v3:campus_total_duration` | `answer_missing_expected_term` | Answered "3小时30分钟"; expected strings included `3.5`, `3 小时 30 分钟`, `三个半小时`. This is a strict-string false negative. |

### DeepSeek V4 Flash Failures

| Case | Failure type | Observed behavior |
| --- | --- | --- |
| `orion_spec_v3:orion_shortest_retention` | `answer_missing_expected_term` | Answered "3天"; expected `3 days`. Semantically correct, but language/form did not match the strict expected string. |
| `orion_spec_v3:orion_not_for_high_stakes` | `answer_missing_expected_term` | Answered "医疗诊断"; expected `medical diagnosis` / `legal representation`. Semantically correct, but language/form did not match. |
| `orion_spec_v3:orion_offline_vs_live` | `answer_missing_expected_term` | Correctly contrasted saved-note reading and lack of new speech transcription, but in Chinese; expected English terms. |
| `campus_workshop_v3:campus_meal_refusal` | `refusal_escape` | Answered "本通知没有提供餐饮补贴金额" instead of using the formal refusal branch. Content is safe, but it fails the strict refusal contract. |
| `campus_workshop_v3:campus_total_duration` | `answer_missing_expected_term` | Answered "3小时30分钟"; same strict-string false negative as Qwen. |

## Semantic Audit

The strict score is the official machine score for this run. However, a manual semantic audit shows that several failures are scoring artifacts rather than genuine content errors:

- Both models correctly computed total workshop duration as `3小时30分钟`.
- Both models answered the meal-subsidy question safely by saying the document does not provide the amount/information, but the scorer expected a formal refusal branch.
- DeepSeek V4 Flash answered three English-document cases in Chinese. The content was semantically correct, but it missed English expected substrings.

If these semantic equivalents are counted as correct, both models are effectively at or near `75 / 75`. The remaining product distinction is not factual accuracy, but output-language consistency and branch-contract compliance.

## Interpretation

This V3 run is more objective than earlier comparisons because it uses newly created documents and harder questions, and it was run without tuning between models.

The practical conclusion is nuanced:

- Qwen has the better **strict machine score** and better English-output conformity on bilingual questions.
- DeepSeek V4 Flash remains a serious candidate: it did not show citation failures, runtime instability, or factual collapse; its raw misses are mostly language/format mismatches.
- Both models share the same refusal-contract weakness on "the document says no information is provided" cases: they answer safely but do not always route to the formal refusal branch.

## Decision For Competition Demo

Keep `qwen3-235b-a22b-instruct-2507` as the default judged/demo model.

Reason:

1. It leads on strict V3 automated score: `73 / 75` vs `70 / 75`.
2. It remains best on the current full regression route: `51 / 51`.
3. It is slightly faster in V3: `5290 ms` vs `5445 ms`.
4. It is more likely to preserve the output language expected by English prompts.

Do not discard `deepseek-v4-flash`. It should stay as a credible candidate for later, especially if the scoring/evaluation layer is upgraded to normalize language variants and semantic equivalents.

## Next Evaluation Improvement

The next truly objective step is to improve the scorer, not just add more questions:

- normalize simple numeric/date expressions (`3小时30分钟` == `3 小时 30 分钟` == `3.5 hours`)
- support bilingual expected-answer aliases
- separate "safe negative answer" from "formal refusal branch" in refusal scoring
- optionally add an LLM-as-judge pass, but only after freezing judge prompts and auditing a sample manually

Until then, use both views:

- strict automated score for reproducibility
- semantic audit for judging whether a model actually misunderstood the document
