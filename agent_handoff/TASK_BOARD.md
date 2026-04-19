# Task Board

## Now

- No hard engineering blocker is currently open
- Real Wuwen Xinqiong minimal-path validation is now done in-project
- A gold-sample candidate PDF plus `2 answerable + 1 refusal` candidate prompts are now locked
- Full gold-sample screenshot pack is now refreshed under the current real runtime
- Ready-to-use PPT / video / poster drafting docs now exist in-repo
- Printable deck / poster HTML prototypes now exist in-repo
- Repo-native deck / poster PDF export script now exists
- Current deck/poster PDF baselines now exist in-repo
- Asset-pack export now includes the deliverables folder and PDF export script
- Timed video subtitle baseline now exists in-repo
- External AI review bundle and review prompt now exist locally
- Review-driven hardening for evidence/screenshot consistency is now landed in code and materials
- Latest gold-sample screenshot pack is now refreshed as `20260419_*` with metadata sidecars
- Latest export bundle now auto-picks the newest screenshot prefix
- Fresh Q2 ask instability is now closed at the code/runtime layer; `3 / 3` fresh local runs returned `declared`
- `G3` operator rehearsal is now recorded as a warm-state pass
- Competition material chain has now been rebuilt from clean source docs
- Printable export now has sanity checks and a clean baseline (`deck.pdf=6` pages, `poster.pdf=1` page)
- If preparing for judging/demo, prioritize final asset production rather than feature work

## Next Best Tasks

1. Export a refreshed competition handoff bundle so the rebuilt `deck/poster` outputs replace the older printable baseline
2. Use `agent_handoff/FREEZE_FACT_SHEET_20260419.md` as the first reference for any further external review or operator handoff
3. Freeze a final submission-oriented material set after one more asset refresh if wording/screenshots change
4. Keep the broader sample-set replay as secondary reference only; use gold-sample replay as the default judging/demo evidence path
5. Before judged demo: set `DEMO_MODE=true` on the target env and verify the opening flow on the target URL

## Recently Verified

- `2026-04-18`: `evidence/samples/chinese_llm_spatial_eval.pdf` completed the real path `upload -> ask -> citation -> PDF render` with `qwen3-235b-a22b-instruct-2507`
- `2026-04-18`: true off-topic ask (`木星有几颗卫星？`) refused correctly with `retrieval_no_match`
- `2026-04-18`: locked gold-sample candidate set in `evidence/materials/GOLD_SAMPLE_CANDIDATE_20260418.json`
- `2026-04-18`: `qwen3-235b-a22b-instruct-2507` and `qwen3-32b` both passed the candidate set; primary remains `qwen3-235b-a22b-instruct-2507`
- `2026-04-18`: replay tooling was updated to the current session/access-token boundary and refreshed `gold_sample_replay_real_*` outputs successfully
- `2026-04-18`: demo/material docs were aligned to the locked gold-sample candidate, including `GOLD_SAMPLE_RUNBOOK.md`
- `2026-04-18`: runtime/deploy/material docs were aligned to the current Wuwen Xinqiong baseline and gold-sample-primary evidence path
- `2026-04-18`: automated browser capture refreshed the four core gold-sample screenshots in `evidence/screenshots/`
- `2026-04-18`: `evidence/materials/COMPETITION_ASSET_PACK.md` was added to map screenshots/reports into final PPT/video/poster assets
- `2026-04-18`: automated browser capture also refreshed `20260418_stats_panel.png` and `20260418_api_docs.png`
- `2026-04-18`: ready-to-use drafting docs were added for PPT (`PPT_DECK_6SLIDES.md`), video (`VIDEO_SHOTLIST_2MIN.md`), and poster (`POSTER_COPY.md`)
- `2026-04-18`: `scripts/export_competition_asset_pack.ps1` can now export a timestamped production bundle for another operator
- `2026-04-18`: printable HTML prototypes were added under `deliverables/competition_kit/` for deck/poster production
- `2026-04-19`: `scripts/export_competition_pdfs.js` can now export deck/poster PDFs directly from the HTML prototypes
- `2026-04-19`: `deliverables/competition_kit/deck.pdf` and `poster.pdf` were exported successfully
- `2026-04-19`: `scripts/export_competition_asset_pack.ps1` now includes the deliverables folder and PDF export script
- `2026-04-19`: `deliverables/competition_kit/video_subtitles.srt` was added as the 2-minute demo subtitle baseline
- `2026-04-19`: external AI review bundle prepared at `review_bundle_stage_20260419_003447/` and zipped as `review_bundle_20260419_003447_competition_ai_review.zip`
- `2026-04-19`: review-driven hardening landed for:
  - preview quote/snippet alignment
  - retrieval-gate refusal semantics
  - stricter screenshot capture (`declared` required for answerable cases)
  - appendix-only handling for stats/api-doc assets
- `2026-04-19`: refreshed screenshot set created as `20260419_*`, with `.json` sidecars for ask/refusal screenshots
- `2026-04-19`: `scripts/export_competition_asset_pack.ps1` now auto-detects the latest screenshot prefix and includes the screenshot sidecars
- `2026-04-19`: `deliverables/competition_kit/deck.pdf` and `poster.pdf` were regenerated against the refreshed screenshots
- `2026-04-19`: Q2 fresh stability check recorded at `evidence/experiments/20260419_q2_declared_stability_check.md`; `3 / 3` runs returned `declared`
- `2026-04-19`: `G3` rehearsal recorded at `evidence/experiments/20260419_g3_rehearsal_template.md`; `3` consecutive runs passed on the locked gold-sample flow
- `2026-04-19`: competition material chain rebuilt from clean docs; printable export now verifies `deck.pdf=6` pages and `poster.pdf=1` page

## Useful But Not Urgent

1. Detail-level replay comparison and report
2. Stronger grounding semantics for `summary` / `outline`
3. More polished competition materials
4. Add expired-session cleanup script

## Do Not Start By Default

1. New task types
2. OCR-heavy work
3. Local-model branch
4. Large frontend redesign
5. Public SaaS scope expansion

## Review Notes

- The strongest narrative remains:
  - evidence-backed document QA for paper/report reading and defense prep
- The weakest narrative remains:
  - generic document platform / open trial SaaS framing
- Refusal demos must use prompts that are purely off-topic; prompts that still mention in-document entities can retrieve and answer
- Current QA recommendation:
  - keep `qwen3-235b-a22b-instruct-2507` as default for stronger broad-answer grounding
  - keep `qwen3-32b` as validated fallback if demo/runtime latency becomes tighter

## Latest Override (`2026-04-19`)

- `G3` should now be treated as closed for the current warm-state judged-demo path
- Authoritative freeze facts now live in:
  - `agent_handoff/FREEZE_FACT_SHEET_20260419.md`
- The latest external final-review artifact is:
  - `review_bundle_stage_20260419_132632/`
  - `review_bundle_20260419_132632_final_competition_review.zip`
- This latest review bundle is preferred over the older broad review pack because it now includes:
  - `PROJECT_CONTEXT.md`
  - refreshed `REVIEW_PROMPT.md`
  - `Q2` stability evidence
  - recorded `G3` pass evidence
- If another AI is asked to review the project now, use this latest bundle first
