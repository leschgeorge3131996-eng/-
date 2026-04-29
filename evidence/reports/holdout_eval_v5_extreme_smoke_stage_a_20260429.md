# V5 Extreme Smoke Stage A - key model comparison

Date: 2026-04-29

## Purpose

This is the first extreme smoke run after the V4 result showed Qwen3 235B and DeepSeek V4 Flash were close. The goal is to screen the highest-priority candidates before running a larger V5 suite.

Manifest: `evidence/materials/HOLDOUT_EVAL_V5_EXTREME_SMOKE_20260429.json`

Scope: 8 documents, 20 cases. Most cases are intentionally hard and cover long-context traps, conflict handling, table/numeric reasoning, explicit missing information, prompt injection, multilingual answering, OCR-like noise, and overlong user requests.

## Models Tested

| Model | Strict Pass | Avg Latency | Refusal Precision | Citation Accuracy | Declaration Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| `qwen3-235b-a22b-instruct-2507` | 18 / 20 | 5211 ms | 50.0% | 94.4% | 94.4% |
| `deepseek-v4-flash` | 17 / 20 | 6388 ms | 100.0% | 94.4% | 94.4% |
| `deepseek-v4-pro` | 17 / 20 | 11506 ms | 50.0% | 94.4% | 94.4% |
| `glm-5.1` | 17 / 20 | 15477 ms | 0.0% | 100.0% | 100.0% |

## Strict Result

Qwen3 235B wins the strict product-contract score in this first Stage A run.

However, the strict table slightly understates DeepSeek V4 Flash and GLM-5.1 because some failures are language/alias artifacts rather than fact failures. For example, Flash correctly answered the education-group exclusion in Chinese, but the strict aliases were English-only. Flash also correctly described the data-protection-officer export control in Chinese, but the expected aliases were English-only.

## Failure Notes

### Qwen3 235B

- `conflict_bundle_v5:taxi_owner_conflict`: refused after retrieval instead of citing the conflict and saying no final owner can be determined.
- `missing_info_contract_v5:rollback_date_value`: answered "No rollback date is provided" with evidence. Semantically safe, but failed the current refusal-contract scorer because it did not return the formal refused outcome.

### DeepSeek V4 Flash

- `long_policy_manual_v5:excluded_group`: semantically correct in Chinese, strict alias miss.
- `conflict_bundle_v5:taxi_owner_conflict`: refused after retrieval instead of citing the conflict.
- `prompt_injection_v5:required_control`: semantically correct in Chinese, strict alias miss.

### DeepSeek V4 Pro

- `conflict_bundle_v5:taxi_owner_conflict`: refused after retrieval instead of citing the conflict.
- `missing_info_contract_v5:explicit_no_rollback`: semantically correct in Chinese, strict alias miss.
- `missing_info_contract_v5:rollback_date_value`: answered "not provided" rather than formal refused outcome.

### GLM-5.1

- `conflict_bundle_v5:taxi_owner_conflict`: semantically correct, strict alias miss.
- `missing_info_contract_v5:rollback_date_value`: answered "not provided" rather than formal refused outcome.
- `ocr_noise_notice_v5:approver_signature`: answered that the damaged signature cannot identify the approver rather than formal refused outcome.

## Interpretation

The current default should not be changed based on Stage A:

- Qwen has the best strict score and fastest average latency among the four key models tested.
- DeepSeek V4 Flash remains the strongest challenger because its strict failures include two likely false negatives and it achieved 100% refusal precision in this run.
- DeepSeek V4 Pro did not justify its slower latency in this product path.
- GLM-5.1 has excellent citation/declaration behavior, but its refusal contract is currently incompatible with the evaluator/product expectation.

## Product-Layer Finding

The biggest recurring issue is not pure model intelligence. It is outcome typing:

- "Document explicitly says no rollback date is provided" can be a valid answer to a meta-question.
- "What is the rollback date?" should surface as structured missing information / refused.
- "There is a conflict and no priority rule" should be an evidence-backed answer, not a generic refusal.

This means the next engineering improvement should be a stronger missing-information and conflict-answer contract, not simply swapping the default model.

## Recommendation

Keep `qwen3-235b-a22b-instruct-2507` as the default for now.

Keep `deepseek-v4-flash` as the first-line challenger and include it in the full V5 run after the scorer is upgraded with multilingual aliases or semantic audit fields.

Do not promote `deepseek-v4-pro` or `glm-5.1` to the live demo path yet.

