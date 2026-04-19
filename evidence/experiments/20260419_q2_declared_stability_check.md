# Q2 Declared Stability Check (`2026-04-19`)

- Goal:
  - verify that the locked Q2 prompt returns `evidence_mode=declared` on fresh real runs
- Prompt:
  - `作者最终的方法排名和总体准确率分别是多少？`
- Document:
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
- Runtime:
  - local backend with current Wuwen Xinqiong `.env`
  - `DEMO_MODE=true`
  - cache cleared before each run

## Result

- `3 / 3` fresh runs returned:
  - `evidence_mode=declared`
  - `used_chunk_count=2`
  - `evidence_quote_count=2`
  - `citation_count=2`
  - answer: `作者最终的方法排名第六，总体准确率为56.20%。`

## Request IDs

1. `785bf35b11e5418f942a7e08d5b33351`
2. `1e38cbd263424988a1880bb286a20fcf`
3. `9df441cc64bc487aa90a59fc66275602`

## Notes

- Earlier manual UI testing reproduced a fresh `candidate` fallback for Q2 even after cache clear.
- The backend now includes a one-step `ask` evidence retry when structured evidence is missing, so a single bad structured-output turn no longer needs to surface directly to the UI.
- In the three fresh runs recorded here, `ask_evidence_retry_count` stayed `0`; the retry safeguard did not need to fire, but it remains as protection against future provider drift.
