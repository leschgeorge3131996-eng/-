# Model strategy and extreme-test plan - 2026-04-29

## Why this exists

The latest V4 holdout changed the model-selection picture. `qwen3-235b-a22b-instruct-2507` and `deepseek-v4-flash` both scored `48 / 50`, so the old framing of "Qwen clearly wins" is no longer accurate. The right next step is to widen the candidate pool and test harsher product risks, not keep repeating short clean-document QA.

## Current evidence

| Evidence | Qwen3 235B | DeepSeek V4 Flash | Notes |
| --- | ---: | ---: | --- |
| Extended V1 fresh | 51 / 51 | 48 / 51 | Qwen still has the strongest historical project regression record. |
| Holdout V3 | 73 / 75 | 70 / 75 | Some strict failures were semantic/format artifacts. |
| Holdout V4 | 48 / 50 | 48 / 50 | Flash is now a first-line candidate, not a weak fallback. |
| V4 citation accuracy | 97.8% | 100.0% | Flash had cleaner citation/declaration behavior in this round. |
| V4 avg latency | 5369 ms | 5482 ms | Difference is too small to decide by speed. |

## Live provider model pool

The current Wuwen Xinqiong-compatible `/models` endpoint exposes these higher-value candidates for another round:

- Stable current default: `qwen3-235b-a22b-instruct-2507`
- DeepSeek V4 family: `deepseek-v4-flash`, `deepseek-v4-pro`
- DeepSeek newer/parallel candidates: `deepseek-v3.2`, `deepseek-v3.2-thinking`, `deepseek-v3.1-terminus`
- Qwen fast/thinking candidates: `qwen3-next-80b-a3b-instruct`, `qwen3-next-80b-a3b-thinking`
- Kimi candidate: `kimi-k2.6`
- Z.AI candidate: `glm-5.1`
- Minimax candidate: `minimax-m2.7`, plus `minimax-m2.5`

Alibaba Cloud official docs list newer flagship Qwen options such as Qwen3-Max/Qwen3.5, but those IDs are not present in the current gateway model list. They should be treated as "possible if we add/verify a different provider path", not as immediate demo candidates.

## Agent consensus

### Default model

Keep `qwen3-235b-a22b-instruct-2507` as the competition default until a stronger candidate passes the same regression stack plus V5 extreme tests.

Reason: Qwen has the thickest project-specific regression record. A newer model is not automatically safer in this product because the real risk is structured evidence, refusal contract, and PDF citation behavior.

### First-line challenger

Promote `deepseek-v4-flash` to first-line challenger.

Reason: V4 tie plus official V4 positioning means Flash is genuinely strong. It should be included in every future model bake-off and can be a credible fallback/candidate.

### High-quality slow mode

Do not expose a high-quality slow mode in the judge UI yet. Test these first:

1. `deepseek-v4-pro`
2. `glm-5.1`
3. `kimi-k2.6`

Reason: all three may be stronger on complex reasoning or long-horizon work, but they have not yet proven stable in this exact RAG/citation/refusal path. `deepseek-v4-pro` previously had provider 500/stall issues, and Kimi was historically too slow for live demo.

### Fast fallback

Keep `qwen3-next-80b-a3b-instruct` as the proven fast fallback for latency emergencies, but retest `deepseek-v4-flash` and `qwen3-next-80b-a3b-thinking` under V5.

## V5 Extreme Holdout design

Recommended size: `100-120` cases across `12-16` documents.

Do not make V5 just "more short questions". It should target real product failure modes:

| Risk axis | Target cases | What it tests |
| --- | ---: | --- |
| Long context | 18 | Far evidence, repeated headings, outdated clauses, appendix traps. |
| Cross-document conflict | 16 | Version priority, unresolved contradictions, errata vs old docs. |
| Table/numeric reasoning | 20 | Multi-row filtering, percentages, unit conversion, date intervals. |
| Missing-information contract | 14 | Distinguish absent info, explicit negative, unresolved conflict. |
| Prompt injection in documents | 12 | Treat document instructions as quoted content, not system orders. |
| Multilingual mixed text | 10 | Chinese/English/Japanese/pinyin/entity aliases, answer-language control. |
| OCR/noisy text | 10 | Recover obvious noise but refuse uncertain fields. |
| Overlong user question | 8 | Extract the real question from noisy user wording. |
| Combined stress | 8-12 | Long + conflict + numeric + refusal in one case. |

## Scoring upgrades

V5 should report both strict contract score and semantic score.

- `retrieval_score`: correct page/chunk hit.
- `answer_score`: fact correctness with partial credit.
- `numeric_score`: typed value with tolerance, not only substring matching.
- `citation_score`: evidence quote covers the decisive fact.
- `refusal_score`: separate `absent_missing`, `explicit_negative`, and `conflict_unresolved`.
- `instruction_safety_score`: document-internal prompt injection ignored.
- `language_score`: output language follows user request.
- `runtime_score`: provider failure and model wrong answer are reported separately.

## Candidate test ladder

Stage A - cheap smoke, `10-12` cases:

- `qwen3-235b-a22b-instruct-2507`
- `deepseek-v4-flash`
- `deepseek-v4-pro`
- `glm-5.1`
- `kimi-k2.6`
- `minimax-m2.7`
- `deepseek-v3.2-thinking`
- `qwen3-next-80b-a3b-thinking`

Stage B - full V5, only top `3-4`:

- Current default
- Best DeepSeek V4 candidate
- Best non-Qwen/non-DeepSeek candidate
- Best fast fallback

Stage C - demo gate:

- Run `scripts/predeploy_sanity.py`
- Run gold sample path
- Check PDF render and citation click-through
- Verify no model switch appears as a judge-visible risky control

## Product decision rule

Switch the default model only if a challenger beats Qwen by at least one of these margins on frozen V5:

- `+5` percentage points strict score, with no worse runtime stability; or
- equal strict score but materially better citation/refusal behavior and lower latency; or
- clear win on extreme cases that map directly to the judged demo story.

Otherwise keep Qwen default and use the challenger as backup or offline comparison evidence.

## Next engineering action

Build V5 Extreme Holdout first, then run Stage A. The most valuable code-side fix before or alongside that is normalizing "document does not provide this information" into the same structured missing-information/refusal outcome across models.

