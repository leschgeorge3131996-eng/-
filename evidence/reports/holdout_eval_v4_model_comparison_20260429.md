# Holdout V4 model comparison - Qwen3 235B vs DeepSeek V4 Flash

Date: 2026-04-29

## Purpose

This round was added after questioning whether the previous tests were too favorable to the existing Qwen default model. V4 is a fresh holdout suite with both easy and hard questions, wider answer aliases, and a broader mix of document types.

The goal is not to rank all general LLM ability. The goal is to decide which model is safer for YanDatong's current RAG answer path, competition demo, citation behavior, and refusal contract.

## Test Design

- Manifest: `evidence/materials/HOLDOUT_EVAL_V4_20260429.json`
- Sample documents: `evidence/samples/holdout_v4/`
- Models tested:
  - `qwen3-235b-a22b-instruct-2507`
  - `deepseek-v4-flash`
- Total cases: 50
- Difficulty mix:
  - Easy: 25
  - Medium: 13
  - Hard: 12
- Task mix:
  - Answerable: 45
  - Refusal / missing-information boundary: 5
- Coverage:
  - Direct facts
  - Dates
  - Numeric extraction
  - Multi-step reasoning
  - Boundary conditions
  - Refusal behavior

## Headline Result

| Model | Passed | Pass Rate | Avg Latency | Answerable Pass | Refusal Precision | Citation Accuracy | Declaration Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen3 235B | 48 / 50 | 96.0% | 5369 ms | 97.8% | 80.0% | 97.8% | 97.8% |
| DeepSeek V4 Flash | 48 / 50 | 96.0% | 5482 ms | 97.8% | 80.0% | 100.0% | 100.0% |

DeepSeek V4 Flash ties Qwen on strict pass rate in this broader V4 holdout. Flash is also slightly stronger on citation/declaration metrics in this run, while Qwen is slightly faster on average by 113 ms. The latency gap is too small to matter for product decision-making.

## Breakdown

| Category | Qwen3 235B | DeepSeek V4 Flash | Comment |
| --- | ---: | ---: | --- |
| Direct fact | 15 / 15 | 15 / 15 | Both stable. |
| Boundary lookup | 5 / 5 | 5 / 5 | Both stable on explicit document-bound answers. |
| Reasoning | 11 / 12 | 11 / 12 | One shared hard grant-comparison failure area. |
| Numeric | 7 / 7 | 7 / 7 | Both stable. |
| Date | 6 / 6 | 6 / 6 | Both stable. |
| Refusal | 4 / 5 | 4 / 5 | Both answered one missing-information question instead of refusing. |

| Difficulty | Qwen3 235B | DeepSeek V4 Flash | Comment |
| --- | ---: | ---: | --- |
| Easy | 25 / 25 | 25 / 25 | No gap. |
| Medium | 12 / 13 | 12 / 13 | Same refusal boundary miss. |
| Hard | 11 / 12 | 11 / 12 | Same grant-comparison area. |

## Failure Review

### Shared issue: missing-information refusal

Case: `api_migration_v4:api_rollback_refusal`

Question: "What rollback date does the note provide?"

Expected behavior: refuse / say the document does not contain a rollback date.

Actual behavior:

- Qwen: answered that the note does not provide a rollback date.
- DeepSeek V4 Flash: answered that the note does not provide a rollback date.

Strict scorer marked both as failures because this case was categorized as a refusal contract test. Semantically, both models recognized the missing field, but the product contract needs this to be represented as a refusal outcome rather than a normal answered outcome.

Decision implication: this is more of a product-level output contract problem than a pure model intelligence problem. The answer pipeline should normalize "not provided in the document" into the same refusal shape used by the UI and scoring harness.

### Grant amount comparison

Case: `grant_rules_v4:grant_amount_gap`

Expected answer: 7 万元.

Observed:

- Qwen hit a provider/runtime disconnect on this one request, so the strict result is a runtime failure rather than a wrong answer.
- DeepSeek V4 Flash returned a completed answer but did not match the expected value.

Decision implication: Qwen's miss is operational stability on a single request; Flash's miss is a reasoning/value error on this case. Both are real risks, but they are different kinds of risk.

## Interpretation

This V4 round materially changes the framing:

- DeepSeek V4 Flash should be treated as a serious candidate, not a weak fallback.
- The current evidence no longer supports saying Qwen is clearly better on model capability.
- For YanDatong's current competition route, Qwen can remain the default because it has more accumulated project regression history and has already been exercised through earlier gold samples.
- DeepSeek V4 Flash should remain available as a candidate/fallback and deserves UI-level A/B comparison if time allows.

## Recommendation

Keep `qwen3-235b-a22b-instruct-2507` as the default for the competition demo, but update our internal wording:

- Do not claim: "Qwen is definitely stronger than DeepSeek V4."
- Claim instead: "On our current RAG/citation/refusal benchmark, Qwen and DeepSeek V4 Flash are effectively tied. We keep Qwen as the demo default because it has more accumulated project-specific regression evidence; DeepSeek V4 Flash is retained as a credible alternative."

The highest-value next technical task is no longer another broad model bake-off. It is tightening the refusal/output contract so missing-information answers are consistently surfaced as "document does not contain this information" in the same structured path across models.

