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

The script now creates its own controlled-alpha session and passes the current
document access token/session boundary automatically, so it matches the current
runtime posture instead of the older pre-session flow.

## One-Click Option

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_real_replay.ps1
```

This wrapper will:

1. replay the fixed sample set with the real model
2. export timestamped replay reports
3. refresh the authoritative `*_latest` replay files
4. export the latest global log summary

You can also target a different manifest and filename prefix, for example the
locked gold-sample candidate:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_real_replay.ps1 -Manifest evidence\materials\GOLD_SAMPLE_CANDIDATE_20260418.json -NamePrefix gold_sample_replay_real
```

## What It Produces

- Timestamped replay reports under `evidence/reports/`
- Authoritative latest files:
  - `evidence/reports/sample_replay_real_latest.md`
  - `evidence/reports/sample_replay_real_summary_latest.md`
- Route tier / route model / route reason
- Outcome, cache hit, retrieval status
- Citation count / source chunk count
- Used chunk count / evidence quote count

## Suggested Evidence To Refresh After Real Replay

1. Screenshot of the frontend summary result
2. Screenshot of the frontend ask result with citations
3. Screenshot of the frontend refused result for an off-topic question
4. Screenshot of the frontend outline result
5. Authoritative latest replay summary
6. If needed, `latest_log_summary.md` as general telemetry only

## Notes

- For clean measurements, keep `--clear-cache`
- For repeatable evidence, do not change prompts between runs
- If one sample fails because of transient provider issues, rerun only after the rate limit window has cooled down
- `latest_log_summary.md` is a global development telemetry summary, not a replay-scoped benchmark report
- If you want the exact locked competition candidate instead of the broader sample set, use the gold-sample manifest rather than `SAMPLE_MANIFEST.json`
