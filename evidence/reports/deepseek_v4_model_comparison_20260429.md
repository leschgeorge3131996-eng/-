# DeepSeek V4 Model Comparison — 2026-04-29

## Decision

Keep `qwen3-235b-a22b-instruct-2507` as the judged/demo default QA model.

Use `deepseek-v4-flash` only as an experimental fast candidate or emergency fallback after a fresh sanity run. Do not use `deepseek-v4-pro` for the current live demo path.

## Runs

### Gold Sample Quick Screen

Report:

- `evidence/reports/gold_sample_qa_compare_deepseek_v4_20260429.md`
- `evidence/reports/gold_sample_qa_compare_deepseek_v4_20260429.json`

| Model | Passed | Avg latency | Max latency | Notes |
| --- | ---: | ---: | ---: | --- |
| `deepseek-v4-flash` | `3 / 3` | `4210 ms` | `6655 ms` | Best quick-screen latency; evidence/citation path worked. |
| `qwen3-235b-a22b-instruct-2507` | `3 / 3` | `5047 ms` | `8021 ms` | Current default remained stable. |
| `deepseek-v4-pro` | `3 / 3` | `8960 ms` | `15087 ms` | Passed but already too slow for the fastest demo path. |

### Full Extended Evaluation

Reports:

- `evidence/reports/extended_eval_v1_qwen3_235b_a22b_instruct_2507_fresh_20260429.md`
- `evidence/reports/extended_eval_v1_deepseek_v4_flash_20260429.md`

| Model | Passed | Pass rate | Answerable | Refusal | Citation | Declaration | Avg latency | Status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `qwen3-235b-a22b-instruct-2507` | `51 / 51` | `100.0%` | `100.0%` | `100.0%` | `100.0%` | `100.0%` | `6448 ms` | Full pass. |
| `deepseek-v4-flash` | `48 / 51` | `94.1%` | `93.0%` | `100.0%` | `97.7%` | `100.0%` | `7542 ms` | Finished, but lost 3 answerable cases. |
| `deepseek-v4-pro` | Incomplete | N/A | N/A | N/A | N/A | N/A | N/A | Gold sample passed, but full eval stalled at `6 / 51`; stopped as impractical for live demo. |

## DeepSeek V4 Flash Failure Triage

`deepseek-v4-flash` kept refusal behavior and evidence declaration stable, but failed 3 medium answerable cases:

| Case | Failure type | Stage | Reason |
| --- | --- | --- | --- |
| `chinese_llm_spatial_eval:zh_a2_prompt_strategies` | `wrong_page` | citation | Cited page `[4]` instead of expected pages `[1, 5, 6]`. |
| `attention_is_all_you_need:en_a2_why_no_recurrence` | `answer_missing_expected_term` | answer | Answer missed expected terms such as `parallel`, `sequential`, `long`, `dependencies`. |
| `attention_is_all_you_need:en_a2_positional_enc` | `answer_missing_expected_term` | answer | Answer missed expected terms such as `sine`, `cosine`, `sinusoid`. |

## Interpretation

- `qwen3-235b-a22b-instruct-2507` remains the only candidate with a fresh `51 / 51` run on the current retrieval/context patch.
- `deepseek-v4-flash` is compatible with the pipeline and safe on refusal in this run, but it is not faster on the full suite and loses accuracy versus the current default.
- `deepseek-v4-pro` has no practical advantage for judging right now: the quick screen was slower than both alternatives, and the full run stalled early.

## Recommendation

For judged demo:

```env
MODEL_QA=qwen3-235b-a22b-instruct-2507
MODEL_SUMMARY=qwen3-235b-a22b-instruct-2507
MODEL_OUTLINE=qwen3-235b-a22b-instruct-2507
```

If live latency becomes the only blocker, prefer the previously validated `qwen3-next-80b-a3b-instruct` fallback before switching to DeepSeek V4 Flash. DeepSeek V4 Flash can stay on the candidate list for another round only if we specifically patch and rerun the three failed cases.
