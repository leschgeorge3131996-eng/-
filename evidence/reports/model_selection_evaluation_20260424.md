# Model Selection Evaluation — 2026-04-24

## Executive Decision

Keep `qwen3-235b-a22b-instruct-2507` as the default `MODEL_QA` for the judged/demo path.

Why:

- It is the best full-suite performer among completed candidates: `48 / 51` on `EXTENDED_EVAL_V1`.
- It has the best answerable pass rate, citation accuracy, and declaration rate among completed full runs.
- It is still fast enough for the current demo path: average latency `3401 ms` on the 51-case run.
- It preserves `100%` refusal precision, matching the core anti-hallucination requirement.

## Scope

This evaluation intentionally separates two layers:

1. **Gold quick screen**: all 8 candidate models on the locked 3-prompt gold sample.
2. **Full extended replay**: 51-case `EXTENDED_EVAL_V1` on the strongest / most relevant candidates.

Gold quick screen is useful for availability and basic compatibility. Full extended replay is the decision source because it stresses:

- Chinese and English documents
- PDF and Markdown samples
- answerable factual questions
- refusal behavior
- citation page hits
- structured evidence declaration

## Candidate Models

Gold quick screen covered:

- `qwen3-235b-a22b-instruct-2507`
- `qwen3-32b`
- `qwen3-next-80b-a3b-instruct`
- `deepseek-v3.2`
- `deepseek-v3.2-thinking`
- `glm-5.1`
- `kimi-k2.6`
- `minimax-m2.7`

Full 51-case replay completed for 8 models:

- `qwen3-235b-a22b-instruct-2507`
- `qwen3-next-80b-a3b-instruct`
- `qwen3-32b`
- `deepseek-v3.2`
- `glm-5.1`
- `deepseek-v3.2-thinking`
- `minimax-m2.7`\r\n- `kimi-k2.6`\r\n\r\n`kimi-k2.6` eventually completed the full 51-case replay at `47 / 51` (`92.2%`) but averaged `61908 ms`, so it is a quality-capable but impractically slow default-path candidate for the current demo.

## Gold Quick Screen

Report files:

- `evidence/reports/gold_sample_qa_compare_8models_latest.md`
- `evidence/reports/gold_sample_qa_compare_8models_latest.json`

All 8 candidates passed the 3-prompt locked gold sample. This confirms basic compatibility but is not sufficient for choosing the default model.

| Model | Gold Pass | Avg Latency (ms) | Max Latency (ms) |
| --- | ---: | ---: | ---: |
| `qwen3-next-80b-a3b-instruct` | `3 / 3` | `1840` | `3072` |
| `qwen3-235b-a22b-instruct-2507` | `3 / 3` | `2638` | `4104` |
| `qwen3-32b` | `3 / 3` | `3694` | `7248` |
| `deepseek-v3.2` | `3 / 3` | `4119` | `8092` |
| `minimax-m2.7` | `3 / 3` | `7100` | `13193` |
| `glm-5.1` | `3 / 3` | `7679` | `13100` |
| `deepseek-v3.2-thinking` | `3 / 3` | `16942` | `29079` |
| `kimi-k2.6` | `3 / 3` | `25235` | `52135` |

## Full 51-Case Results

Report files are named `evidence/reports/extended_eval_v1_<model>.md` and `.json`.

| Rank | Model | Passed | Pass Rate | Answerable | Refusal | Citation | Declaration | Avg Latency (ms) |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `qwen3-235b-a22b-instruct-2507` | `48 / 51` | `94.1%` | `93.0%` | `100.0%` | `93.0%` | `93.0%` | `3401` |
| 2 | `kimi-k2.6` | `47 / 51` | `92.2%` | `90.7%` | `100.0%` | `90.7%` | `90.7%` | `61908` |`r`n| 3 | `qwen3-next-80b-a3b-instruct` | `46 / 51` | `90.2%` | `88.4%` | `100.0%` | `88.4%` | `90.7%` | `2072` |
| 4 | `deepseek-v3.2` | `45 / 51` | `88.2%` | `86.0%` | `100.0%` | `90.7%` | `90.7%` | `5047` |
| 5 | `qwen3-32b` | `45 / 51` | `88.2%` | `86.0%` | `100.0%` | `86.0%` | `90.7%` | `5209` |
| 6 | `glm-5.1` | `45 / 51` | `88.2%` | `86.0%` | `100.0%` | `86.0%` | `90.7%` | `8346` |
| 7 | `deepseek-v3.2-thinking` | `44 / 51` | `86.3%` | `83.7%` | `100.0%` | `86.0%` | `90.7%` | `36305` |
| 8 | `minimax-m2.7` | `32 / 51` | `62.7%` | `58.1%` | `87.5%` | `58.1%` | `60.5%` | `20121` |

## Interpretation

### Default QA Model

Use `qwen3-235b-a22b-instruct-2507`.

It wins the full suite by a meaningful margin:

- `+1` case over `kimi-k2.6` and `+2` cases over `qwen3-next-80b-a3b-instruct`
- `+3` cases over `deepseek-v3.2`, `qwen3-32b`, and `glm-5.1`
- far better reliability than `minimax-m2.7`

The current project is scored more on citation faithfulness and refusal safety than raw generation style, so full-suite accuracy matters more than quick-screen speed.

### Fast Fallback

Use `qwen3-next-80b-a3b-instruct` as the best speed fallback.

It is the fastest completed full replay (`2072 ms` average) and still keeps `100%` refusal precision, but it loses two more extended cases than the current 235B model.

### Conservative Backup

Keep `qwen3-32b` as a known fallback because it has historical validation and completed the full replay at `45 / 51`.

It is not better than `qwen3-next-80b-a3b-instruct` in this run, but it remains useful if Next availability changes.

### Not Recommended As Default

- `deepseek-v3.2-thinking`: too slow for judged demos and lower full-suite score than 235B.
- `glm-5.1`: acceptable but slower and not more accurate than Qwen alternatives.
- `minimax-m2.7`: not suitable for the current structured-evidence QA pipeline.
- `kimi-k2.6`: quality is second-best (`47/51`) but latency is too high for the default demo path (avg `61908 ms`).

## Recommended Environment Strategy

For demo / judging:

```env
MODEL_QA=qwen3-235b-a22b-instruct-2507
MODEL_SUMMARY=qwen3-235b-a22b-instruct-2507
MODEL_OUTLINE=qwen3-235b-a22b-instruct-2507
```

If live latency becomes the blocker, switch only QA after a final predeploy sanity run:

```env
MODEL_QA=qwen3-next-80b-a3b-instruct
```

Do not switch to MiniMax for the default path; do not switch to Kimi for the default path unless latency requirements change substantially.

## Tooling Change

`scripts/extended_eval.py` now supports:

```bash
python scripts/extended_eval.py --model qwen3-next-80b-a3b-instruct \
  --output evidence/reports/extended_eval_v1_qwen3_next_80b_a3b_instruct.md \
  --json-output evidence/reports/extended_eval_v1_qwen3_next_80b_a3b_instruct.json
```

This lets future agents compare model candidates without editing `.env`.

## Related Product Fix

This run also includes a retrieval improvement for metadata/name questions: product-name queries such as `这个产品的名字是什么？` now trigger the first chunk as a metadata fallback when lexical overlap is otherwise weak. This closes the prior `research_brief:rb_a1_name` failure mode in the local regression path.

