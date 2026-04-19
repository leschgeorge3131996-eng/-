# Submission Prep Guide

## What This Is

This guide explains how to turn the current repository state into a clean
competition/demo submission package.

At the current stage, the locked gold-sample path is the primary submission
story. Broader replay outputs are secondary supporting material only.

## Recommended Submission Set

### Final judged package

1. final `3`-page PPT
2. final `5`-minute solution/demo video
3. `PRODUCT_TECHNICAL_WRITEUP.md`
4. `PLATFORM_USAGE_EVIDENCE.md`
5. `HARD_EVIDENCE_SUMMARY.md`
6. `SCORING_EVIDENCE_MATRIX.md`
7. refreshed gold-sample screenshots

### Production inputs

1. `PROJECT_ONE_PAGER.md`
2. `DEMO_SCRIPT_3MIN.md`
3. `GOLD_SAMPLE_RUNBOOK.md`
4. `COMPETITION_ASSET_PACK.md`
5. `PPT_DECK_6SLIDES.md`
6. `VIDEO_SHOTLIST_2MIN.md`
7. `POSTER_COPY.md`
8. `evidence/reports/gold_sample_replay_real_summary_latest.md`
9. `evidence/reports/gold_sample_qa_compare_latest.md`

### Nice-to-have

1. `ARCHITECTURE.md`
2. `QA_BRIEF.md`
3. one experiment note for the locked gold-sample validation
4. appendix-only stats-panel screenshot
5. appendix-only backend API-docs screenshot

## Spec Crosswalk

Before final export, align the repo assets against the official submission format:

1. `3`-page PPT
2. `5`-minute solution/demo video
3. product and technical document
4. platform usage evidence
5. final screenshot set

Use:

- `SUBMISSION_SPEC_CROSSWALK.md`
- `HANDOFF_PACKAGE_BOUNDARY.md`

Important:

- `PPT_DECK_6SLIDES.md` and `deliverables/competition_kit/deck.pdf` are current content baselines, not the final `3`-page submission deck.
- `VIDEO_SHOTLIST_2MIN.md` and `video_subtitles.srt` are current story baselines, not the final `5`-minute submission video.
- `PROJECT_ONE_PAGER.md`, `DEMO_SCRIPT_3MIN.md`, and `POSTER_COPY.md` are also source materials, not official substitutes for the final judged package.

## One-Click Export

Use the export script when you need a clean handoff bundle for PPT/video/poster
production:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\export_competition_asset_pack.ps1
```

What it does:

- copies the locked gold-sample documents, reports, screenshots, and sample PDF
- copies the judge-facing proof pages and package-boundary docs
- includes the ready-to-use PPT/video/poster drafting docs
- includes the current HTML/PDF deliverables under `deliverables/competition_kit/`
- includes the timed subtitle baseline `deliverables/competition_kit/video_subtitles.srt`
- writes `PACK_CONTENTS.md` into a timestamped export directory under
  `evidence/exports/`

Recommended boundary:

- main submission: final `3`-page PPT, final `5`-minute video, product/technical write-up, platform proof, hard-evidence summary, scoring matrix, final screenshots
- appendix: replay reports, experiment notes, runbook, QA brief, appendix-only screenshots
- ops/source: one-pager, demo script, asset pack, `6`-page deck baseline, `2`-minute video baseline, poster copy, HTML prototypes, export scripts

## HTML Draft Deliverables

If you want a near-final visual baseline before moving into PowerPoint or a
design tool, use:

- `deliverables/competition_kit/deck.html`
- `deliverables/competition_kit/poster.html`

These files are aligned to the same locked gold-sample wording and can be
printed to PDF directly from a browser.

If you want the repo to generate the PDFs directly, run:

```powershell
node .\scripts\export_competition_pdfs.js
```

## How To Present The Project

### Product positioning

- A document assistant for paper/report reading and defense preparation
- Strongest differentiator is evidence-backed QA rather than generic generation

### Core value

- Upload document
- Parse structure
- Retrieve evidence
- Answer with citations
- Jump back to PDF evidence
- Refuse off-topic asks when retrieval does not match

### Why it is not a chat shell

- It preserves page-aware document structure
- It uses retrieval before answering
- It returns citations and evidence snippets
- It can jump back into the cited PDF page
- It logs replay evidence and comparison artifacts

## Suggested Demo Story

1. Show the locked gold-sample candidate
2. Run the first answerable ask
3. Open the cited PDF render
4. Run the second answerable ask
5. Run the off-topic refusal
6. Close with the replay summary and model decision

## Suggested Final Check Before Submission

- [ ] Locked prompts still match `GOLD_SAMPLE_CANDIDATE_20260418.json`
- [ ] `gold_sample_replay_real_summary_latest.md` is current
- [ ] `gold_sample_qa_compare_latest.md` is current
- [ ] The four gold-sample screenshots are current
- [ ] `PPT_DECK_6SLIDES.md`, `VIDEO_SHOTLIST_2MIN.md`, and `POSTER_COPY.md` are still aligned with the same fixed wording
- [ ] `deliverables/competition_kit/deck.html` and `poster.html` still match the same locked story
- [ ] One-pager, demo script, and asset pack all use the same product positioning
- [ ] No broad-sample or historical provider artifact is being presented as the primary judging evidence
