# V6 Extreme Full - Qwen3 235B vs DeepSeek V4 Flash

Date: 2026-04-30

## Purpose

This round expands the prior V5 smoke test into a larger and harder V6 full holdout. The goal is to compare the current default `qwen3-235b-a22b-instruct-2507` against the strongest challenger `deepseek-v4-flash` under more extreme product conditions.

Manifest: `evidence/materials/HOLDOUT_EVAL_V6_EXTREME_FULL_20260430.json`

Scope:

- 12 documents
- 72 total cases
- 59 answerable cases
- 13 refusal / missing-information cases
- 45 hard cases
- Coverage includes long-context traps, cross-version conflict, tables, explicit missing information, prompt injection, multilingual clauses, OCR ambiguity, overlong user prompts, nested exceptions, date intervals, entity aliases, and adversarial citation traps.

## Headline Result

| Model | Strict Pass | Avg Latency | Refusal Precision | Citation Accuracy | Declaration Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| `qwen3-235b-a22b-instruct-2507` | 59 / 72 | 5516 ms | 61.5% | 86.4% | 86.4% |
| `deepseek-v4-flash` | 64 / 72 | 5870 ms | 69.2% | 98.3% | 98.3% |

DeepSeek V4 Flash wins this larger extreme set by `+5` strict cases, with much stronger citation/declaration behavior. Qwen remains slightly faster by about `354 ms` on average, but the latency gap is small compared with the quality/citation gap.

## Category Comparison

| Category | Qwen3 235B | DeepSeek V4 Flash | Readout |
| --- | ---: | ---: | --- |
| Boundary | 3 / 3 | 3 / 3 | Tie |
| Citation traps | 5 / 5 | 4 / 5 | Qwen wins |
| Conflict | 2 / 3 | 2 / 3 | Tie |
| Date | 2 / 2 | 1 / 2 | Qwen wins |
| Date numeric | 2 / 2 | 2 / 2 | Tie |
| Entity aliases | 1 / 5 | 5 / 5 | Flash wins strongly |
| Facts | 6 / 7 | 7 / 7 | Flash wins |
| Prompt injection | 5 / 5 | 4 / 5 | Qwen wins |
| Long context | 1 / 2 | 2 / 2 | Flash wins |
| Missing information | 1 / 1 | 1 / 1 | Tie |
| Multilingual | 6 / 6 | 6 / 6 | Tie |
| Nested rules | 4 / 4 | 4 / 4 | Tie |
| OCR noise | 3 / 3 | 3 / 3 | Tie |
| Overlong user prompt | 1 / 1 | 1 / 1 | Tie |
| Refusal | 8 / 13 | 9 / 13 | Flash wins |
| SLA | 2 / 2 | 2 / 2 | Tie |
| Table / numeric | 5 / 5 | 5 / 5 | Tie |
| Traps | 2 / 3 | 3 / 3 | Flash wins |

## Failure Pattern

### Qwen3 235B

Qwen failures are concentrated in two areas:

- `missing_citation`: 8 failures
- `refusal_escape`: 5 failures

The largest practical weakness is entity-alias handling under the strict evidence contract. It scored only `1 / 5` on entity aliases because several answers reached a matched retrieval state but did not produce declared evidence/citations.

### DeepSeek V4 Flash

Flash failures are more spread out:

- `refusal_escape`: 4 failures
- `answer_missing_expected_term`: 3 failures
- `model_refused_after_retrieval`: 1 failure

Flash's main remaining risks are still output-contract related: formal missing-information behavior, one unresolved-conflict refusal, and a few strict alias/language misses. Its citation/declaration score is much stronger than Qwen in this V6 run.

## Interpretation

This V6 full run is the first test where DeepSeek V4 Flash clearly beats the current Qwen default under a larger and harsher suite.

The result changes the recommendation from:

> "Qwen default, Flash first-line challenger"

to:

> "Flash is now a credible default-candidate and deserves a controlled switch rehearsal."

It still should not be switched blindly in the live judged path without a short validation gate, because:

- V5 manual quality audit found Flash sometimes answers English questions in Chinese.
- Both models still need a better missing-information/conflict outcome contract.
- Qwen remains slightly faster and has more accumulated project history.

## Decision Recommendation

Do not immediately flip the production/demo default in `.env` yet.

Do run the next controlled step:

1. Add a stronger output-language instruction: answer in the user's language unless the user requests otherwise.
2. Add a clearer missing-information/conflict contract: distinguish absent value, explicit negative statement, unresolved conflict, and true out-of-scope refusal.
3. Rerun V6 for Qwen and Flash only.
4. If Flash still leads by at least `+3` strict cases and passes the gold/predeploy sanity path, switch `MODEL_QA` to `deepseek-v4-flash` for a rehearsal branch.

Current operational recommendation:

- Competition default today: keep `qwen3-235b-a22b-instruct-2507`.
- Candidate for switch after one more gate: `deepseek-v4-flash`.
- Do not continue broad model expansion until the Qwen vs Flash decision is settled.

