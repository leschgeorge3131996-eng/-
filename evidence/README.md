# Evidence Directory

Use this directory to store reproducible project evidence for demos, reviews, and competition materials.

## Suggested Structure

- `screenshots/`
  - frontend success pages
  - API docs page
  - log evidence screenshots
- `reports/`
  - exported log summaries
  - comparison notes
  - sample replay reports
  - sample replay summaries
  - use `sample_replay_real_latest.md` and `sample_replay_real_summary_latest.md` as the authoritative real replay outputs
  - treat `latest_log_summary.md` as global development telemetry unless a replay-specific scope is explicitly stated
- `experiments/`
  - experiment records
  - prompt or model comparison notes
- `materials/`
  - one-page project summary
  - demo script
  - sample set
  - architecture description
  - evidence refresh checklist
  - submission prep guide

## Naming Convention

Use a stable pattern:

`YYYYMMDD_topic_detail.ext`

Examples:

- `20260415_summary_success.png`
- `20260415_api_docs.png`
- `20260415_log_summary.md`
