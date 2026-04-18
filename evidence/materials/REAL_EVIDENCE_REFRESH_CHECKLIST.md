# Real Evidence Refresh Checklist

## Goal

After running the fixed sample set with the real cloud model, refresh the evidence package so the demo, logs, and materials all reflect the same current version.

At the current stage, the preferred refresh target is the locked gold-sample candidate rather than the older broad sample set.

## Step 1: Replay With Real Model

Run:

```powershell
.venv\Scripts\python.exe scripts\replay_sample_set.py --clear-cache --format md --output evidence\reports\sample_replay_real.md --timestamped
```

For the locked gold-sample candidate, prefer:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_real_replay.ps1 -Manifest evidence\materials\GOLD_SAMPLE_CANDIDATE_20260418.json -NamePrefix gold_sample_replay_real
```

## Step 2: Refresh Reports

- [ ] Export latest log summary:

```powershell
python scripts\export_log_summary.py --format md --output evidence\reports\latest_log_summary.md
```

- [ ] Keep the timestamped replay report created in `evidence/reports/`

## Step 3: Refresh Screenshots

Capture at least these:

- [ ] Frontend ask result with citations for `这篇论文主要研究了什么问题？`
- [ ] PDF render/evidence page opened from that citation
- [ ] Frontend ask result for `作者最终的方法排名和总体准确率分别是多少？`
- [ ] Frontend refused result for `木星有几颗卫星？`
- [ ] Frontend stats panel
- [ ] Backend API docs page

Recommended naming:

- `YYYYMMDD_gold_ask_research_focus.png`
- `YYYYMMDD_gold_pdf_render.png`
- `YYYYMMDD_gold_ask_rank_accuracy.png`
- `YYYYMMDD_gold_refusal.png`
- `YYYYMMDD_stats_panel.png`
- `YYYYMMDD_api_docs.png`

## Step 4: Refresh Evidence Notes

- [ ] Update experiment note in `evidence/experiments/`
- [ ] Record whether the run used mock or real model
- [ ] Record the active endpoint/model names
- [ ] Record whether route tiering was enabled

## Step 5: Material Alignment

- [ ] Make sure one-pager, demo script, and sample set still match the current UI and backend behavior
- [ ] Make sure the locked gold-sample runbook still matches the current UI and backend behavior
- [ ] If the wording changes, update:
  - `PROJECT_ONE_PAGER.md`
  - `DEMO_SCRIPT_3MIN.md`
  - `SAMPLE_SET.md`
  - `GOLD_SAMPLE_RUNBOOK.md`

## Done Criteria

- [ ] Evidence reports are refreshed
- [ ] Screenshots are refreshed
- [ ] Experiment note is updated
- [ ] Materials reflect the current product behavior
