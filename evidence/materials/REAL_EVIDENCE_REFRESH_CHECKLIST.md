# Real Evidence Refresh Checklist

## Goal

After running the fixed sample set with the real cloud model, refresh the evidence package so the demo, logs, and materials all reflect the same current version.

## Step 1: Replay With Real Model

Run:

```powershell
.venv\Scripts\python.exe scripts\replay_sample_set.py --clear-cache --format md --output evidence\reports\sample_replay_real.md --timestamped
```

## Step 2: Refresh Reports

- [ ] Export latest log summary:

```powershell
python scripts\export_log_summary.py --format md --output evidence\reports\latest_log_summary.md
```

- [ ] Keep the timestamped replay report created in `evidence/reports/`

## Step 3: Refresh Screenshots

Capture at least these:

- [ ] Frontend summary result
- [ ] Frontend ask result with citations
- [ ] Frontend refused result for an off-topic question
- [ ] Frontend outline result
- [ ] Frontend stats panel
- [ ] Backend API docs page

Recommended naming:

- `YYYYMMDD_summary_success.png`
- `YYYYMMDD_ask_with_citations.png`
- `YYYYMMDD_ask_refused.png`
- `YYYYMMDD_outline_success.png`
- `YYYYMMDD_stats_panel.png`
- `YYYYMMDD_api_docs.png`

## Step 4: Refresh Evidence Notes

- [ ] Update experiment note in `evidence/experiments/`
- [ ] Record whether the run used mock or real model
- [ ] Record the active endpoint/model names
- [ ] Record whether route tiering was enabled

## Step 5: Material Alignment

- [ ] Make sure one-pager, demo script, and sample set still match the current UI and backend behavior
- [ ] If the wording changes, update:
  - `PROJECT_ONE_PAGER.md`
  - `DEMO_SCRIPT_3MIN.md`
  - `SAMPLE_SET.md`

## Done Criteria

- [ ] Evidence reports are refreshed
- [ ] Screenshots are refreshed
- [ ] Experiment note is updated
- [ ] Materials reflect the current product behavior

