# Real Replay Guide

## Goal

Use the fixed sample set to replay the current system with the real cloud model and collect reproducible evidence.

## Before You Run

1. Ensure `.env` contains the real provider and valid credentials.
2. Ensure frontend/backend can already run locally.
3. Make sure you understand this replay will consume real quota and tokens.

## Recommended Command

```powershell
.venv\Scripts\python.exe scripts\replay_sample_set.py --clear-cache --format md --output evidence\reports\sample_replay_real.md --timestamped
```

## What It Produces

- A replay report under `evidence/reports/`
- Route tier / route model / route reason
- Outcome, cache hit, retrieval status
- Citation count / source chunk count

## Suggested Evidence To Refresh After Real Replay

1. Screenshot of the frontend summary result
2. Screenshot of the frontend ask result with citations
3. Screenshot of the frontend refused result for an off-topic question
4. Screenshot of the frontend outline result
5. Latest `latest_log_summary.md`
6. Latest real replay report

## Notes

- For clean measurements, keep `--clear-cache`
- For repeatable evidence, do not change prompts between runs
- If one sample fails because of transient provider issues, rerun only after the rate limit window has cooled down

