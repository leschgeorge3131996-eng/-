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

For the core four gold-sample screenshots, you can now also run:

```powershell
node scripts\capture_gold_sample_screenshots.js
```

## Step 2: Refresh Reports

- [ ] Export latest log summary:

```powershell
python scripts\export_log_summary.py --format md --output evidence\reports\latest_log_summary.md
```

- [ ] Keep the timestamped replay report created in `evidence/reports/`

## Step 3: Refresh Screenshots

Capture at least these:

- [ ] Frontend ask result with citations for `杩欑瘒璁烘枃涓昏鐮旂┒浜嗕粈涔堥棶棰橈紵`
- [ ] PDF render/evidence page opened from that citation
- [ ] Frontend ask result for `浣滆€呮渶缁堢殑鏂规硶鎺掑悕鍜屾€讳綋鍑嗙‘鐜囧垎鍒槸澶氬皯锛焋
- [ ] Frontend refused result for `鏈ㄦ槦鏈夊嚑棰楀崼鏄燂紵`
- [ ] Frontend stats panel
- [ ] Backend API docs page

Latest automated gold-sample capture on `2026-04-19` produced:

- `20260529_gold_ask_research_focus.png`
- `20260529_gold_pdf_render.png`
- `20260529_gold_ask_rank_accuracy.png`
- `20260529_gold_refusal.png`
- `20260419_stats_panel.png`
- `20260419_api_docs.png`

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

