# Final Submission Checklist

## Goal

Turn the current repository into a single clean competition submission package
without reopening scope.

## Background And Target

- Judge this project as a competition work aiming at `national first prize`,
  not as a generic SaaS/platform pitch.
- The strongest current product story is evidence-backed document QA for
  paper/report reading and defense preparation.
- The locked judged-demo path is:
  - `upload -> ask -> citation -> PDF -> refusal`
- As of `2026-04-20`, the main remaining gap is no longer feature work. It is:
  - final native `3`-page PPT production
  - final edited/rendered `5`-minute video production
  - final package and wording consistency

## Status Snapshot (`2026-04-20`)

- [x] strict `G3` evidence recorded in
  `evidence/experiments/20260420_g3_strict_rehearsal.md`
- [x] judge-facing proof pages aligned to the same locked story
- [x] official `3`-page deck source exists in `PPT_DECK_3PAGES_FINAL.md`
- [x] official `5`-minute video source exists in
  `VIDEO_SHOTLIST_5MIN_FINAL.md`
- [x] repo-native `3`-page deck baseline exists in
  `deliverables/competition_kit/deck_3page_final.pdf`
- [x] repo-native `5`-minute subtitle baseline exists in
  `deliverables/competition_kit/video_subtitles_5min_final.srt`
- [ ] final native `3`-page PPT file produced
- [ ] final edited/rendered `5`-minute video produced

## Stop-Ship Items

Do not call the package final if any item below is still open.

- [ ] No final native `3`-page PPT file yet
- [ ] No final `5`-minute video file yet
- [ ] Any high-visibility doc still leads with `PPT_DECK_6SLIDES.md` or
  `VIDEO_SHOTLIST_2MIN.md` instead of the final path
- [ ] The final screenshot set does not match the target demo environment and
  there is no explicit freeze decision
- [ ] Any final material claims broader general stability than the locked
  judged-demo evidence actually proves

## Final Freeze Checklist

### 1. Final Judged Assets

- [ ] Create the final native `3`-page PPT from
  `PPT_DECK_3PAGES_FINAL.md` plus
  `deliverables/competition_kit/deck_3page_final.pdf`
- [ ] Create the final `5`-minute video from
  `VIDEO_SHOTLIST_5MIN_FINAL.md` plus
  `deliverables/competition_kit/video_subtitles_5min_final.srt`
- [ ] Ensure the final PPT/video filenames, cover wording, and version labels
  are stable and do not still look like drafts
- [ ] Ensure no slide/subtitle still shows words such as `draft`, `baseline`,
  `candidate`, `current`, or `next step`

### 2. Evidence And Claim Alignment

- [ ] `PRODUCT_TECHNICAL_WRITEUP.md`, `PLATFORM_USAGE_EVIDENCE.md`,
  `HARD_EVIDENCE_SUMMARY.md`, `SCORING_EVIDENCE_MATRIX.md`, the final PPT,
  and the final video all describe the same product positioning
- [ ] `G3` wording stays at strict fresh-upload `3`-run judged-demo
  reproducibility, not open-domain generalization
- [ ] The strongest claim remains evidence-backed `ask`, not generic
  `summary` / `outline`
- [ ] The main story stays `upload -> ask -> citation -> PDF -> refusal`

### 3. Screenshots And Demo Evidence

- [ ] The four core screenshots are current or intentionally frozen:
  - `evidence/screenshots/20260419_gold_ask_research_focus.png`
  - `evidence/screenshots/20260419_gold_pdf_render.png`
  - `evidence/screenshots/20260419_gold_ask_rank_accuracy.png`
  - `evidence/screenshots/20260419_gold_refusal.png`
- [ ] If the target demo environment changed, refresh screenshots before final
  export
- [ ] If screenshots are intentionally reused, keep the spoken story and final
  materials consistent with those exact frozen images

### 4. Material Hygiene

- [ ] `MATERIALS_INDEX.md` and `PRODUCT_TECHNICAL_WRITEUP.md` still point to
  the `3`-page / `5`-minute final path as the primary judged-material route
- [ ] Historical `6`-slide / `2`-minute assets remain archive baselines only
- [ ] No old-provider wording or stale runtime label appears in visible final
  materials
- [ ] `PROJECT_ONE_PAGER.md`, `DEMO_SCRIPT_3MIN.md`,
  `COMPETITION_ASSET_PACK.md`, and `QA_BRIEF.md` all stay aligned with the
  same judged story

### 5. Final Packaging

- [ ] Main submission package contains:
  - final native `3`-page PPT
  - final `5`-minute video
  - `PRODUCT_TECHNICAL_WRITEUP.md`
  - `PLATFORM_USAGE_EVIDENCE.md`
  - `HARD_EVIDENCE_SUMMARY.md`
  - `SCORING_EVIDENCE_MATRIX.md`
  - final screenshot set
- [ ] Appendix package contains only supporting evidence and does not replace
  the main judged assets
- [ ] Exported handoff pack still includes the final-source drafts and repo
  baselines for future operators

## Last Pre-Submission Pass

- [ ] Review `SUBMISSION_SPEC_CROSSWALK.md`
- [ ] Review `HANDOFF_PACKAGE_BOUNDARY.md`
- [ ] Review `DEFENSE_DEMO_RISK_CHECKLIST.md`
- [ ] Confirm the package would still make sense to a new operator opening the
  repo cold

## Out Of Scope Right Now

- New features
- OCR rebuilds
- Local-model branch work
- Large UI redesign
- Public SaaS/platform expansion

