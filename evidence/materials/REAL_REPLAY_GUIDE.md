# Real Replay Guide

## Goal

Use the current real-provider path to replay the system and collect reproducible
evidence. For judging/demo work, the locked gold-sample candidate should now be
treated as the default replay target.

## Before You Run

1. Ensure `.env` contains the current `Wuwen Xinqiong` provider settings and valid credentials.
2. Ensure frontend/backend can already run locally.
3. Make sure you understand this replay will consume real quota and tokens.

## Recommended Command

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_real_replay.ps1 -Manifest evidence\materials\GOLD_SAMPLE_CANDIDATE_20260418.json -NamePrefix gold_sample_replay_real
```

This is the current authoritative judging/demo replay path. The wrapper creates
its own controlled-alpha session and passes the current document
access-token/session boundary automatically, so it matches the live runtime
posture instead of the older pre-session flow.

## Broader Coverage Option

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_real_replay.ps1
```

The default wrapper still exists for the broader fixed sample set. Use it when
you want wider capability coverage rather than the locked competition path.

## What It Produces

- Timestamped replay reports under `evidence/reports/`
- Authoritative latest files for the locked judging/demo path:
  - `evidence/reports/gold_sample_replay_real_latest.md`
  - `evidence/reports/gold_sample_replay_real_summary_latest.md`
- Secondary broader-coverage latest files:
  - `evidence/reports/sample_replay_real_latest.md`
  - `evidence/reports/sample_replay_real_summary_latest.md`
- Route tier / route model / route reason
- Outcome, cache hit, retrieval status
- Citation count / source chunk count
- Used chunk count / evidence quote count

## Suggested Evidence To Refresh After Real Replay

1. Screenshot of the frontend answerable `ask` result with citations
2. Screenshot of the cited PDF render / evidence page
3. Screenshot of the second answerable `ask`
4. Screenshot of the off-topic refusal result
5. `evidence/reports/gold_sample_replay_real_summary_latest.md`
6. `evidence/reports/gold_sample_qa_compare_latest.md` if you need to justify the current QA-model choice

## Notes

- For clean measurements, keep `--clear-cache`
- For repeatable evidence, do not change prompts between runs
- If one sample fails because of transient provider issues, rerun only after the cooldown window
- `latest_log_summary.md` is a global development telemetry summary, not a replay-scoped benchmark report
- Treat the locked gold-sample replay as the authoritative judging/demo evidence path
- Treat the broader `SAMPLE_MANIFEST.json` replay as secondary coverage, not the default competition story
