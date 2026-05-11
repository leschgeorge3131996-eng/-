# Competition Asset Pack

## Goal

Turn the locked gold-sample facts into a single consistent source for:

- PPT
- demo video
- poster
- spoken defense wording

Do not rebuild the story from scratch each time. Reuse this pack.

## Locked Source Of Truth

- Product positioning:
  - evidence-backed document QA for paper/report reading and defense preparation
- Locked sample document:
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
- Locked prompt manifest:
  - `evidence/materials/GOLD_SAMPLE_CANDIDATE_20260418.json`
- Current primary QA model:
  - `deepseek-v4-flash` (switched after V6 contract-patch holdout — see `evidence/reports/holdout_eval_v6_contract_patch_qwen_vs_flash_20260430.md`)
- Current rollback QA fallback:
  - `qwen3-235b-a22b-instruct-2507`
- Current summary / outline model:
  - `qwen3-235b-a22b-instruct-2507`
- Historical validated fallback QA model:
  - `qwen3-32b`
- Current authoritative reports:
  - `evidence/reports/gold_sample_qa_compare_latest.md`
  - `evidence/reports/gold_sample_replay_real_summary_latest.md`
  - `evidence/reports/gold_sample_replay_real_latest.md`
- Current authoritative screenshots:
  - `evidence/screenshots/20260419_gold_ask_research_focus.png`
  - `evidence/screenshots/20260419_gold_pdf_render.png`
  - `evidence/screenshots/20260419_gold_ask_rank_accuracy.png`
  - `evidence/screenshots/20260419_gold_refusal.png`
- Appendix-only supporting screenshots already available:
  - `evidence/screenshots/20260419_stats_panel.png`
  - `evidence/screenshots/20260419_api_docs.png`

## Ready-To-Use Deliverables

- Official `3`-page deck source:
  - `evidence/materials/PPT_DECK_3PAGES_FINAL.md`
- Official `5`-minute video source:
  - `evidence/materials/VIDEO_SHOTLIST_5MIN_FINAL.md`
- Repo-native official deck baseline:
  - `deliverables/competition_kit/deck_3page_final.html`
  - `deliverables/competition_kit/deck_3page_final.pdf`
- PPT page copy:
  - `evidence/materials/PPT_DECK_6SLIDES.md`
- Video shotlist:
  - `evidence/materials/VIDEO_SHOTLIST_2MIN.md`
- Poster copy:
  - `evidence/materials/POSTER_COPY.md`
- Freeze-control docs:
  - `evidence/materials/FINAL_SUBMISSION_CHECKLIST.md`
  - `evidence/materials/DEFENSE_DEMO_RISK_CHECKLIST.md`
- Printable deck/poster prototypes:
  - `deliverables/competition_kit/deck.html`
  - `deliverables/competition_kit/poster.html`
- Current printable PDF baselines:
  - `deliverables/competition_kit/deck_3page_final.pdf`
  - `deliverables/competition_kit/deck.pdf`
  - `deliverables/competition_kit/poster.pdf`
- Video subtitle baseline:
  - `deliverables/competition_kit/video_subtitles_5min_final.srt`
  - `deliverables/competition_kit/video_subtitles.srt`
- One-click export script:
  - `scripts/export_competition_asset_pack.ps1`
- PDF export script:
  - `scripts/export_competition_pdfs.js`

## Official Submission Drafts

- `PPT_DECK_3PAGES_FINAL.md`
  - current repo source draft for the official `3`-page submission deck
  - current repo-native printable baseline:
    - `deliverables/competition_kit/deck_3page_final.html`
    - `deliverables/competition_kit/deck_3page_final.pdf`
  - use this first; keep `PPT_DECK_6SLIDES.md` only as the compression baseline
- `VIDEO_SHOTLIST_5MIN_FINAL.md`
  - current repo source draft for the official `5`-minute submission video
  - current repo-native timing baseline:
    - `deliverables/competition_kit/video_subtitles_5min_final.srt`
  - use this first; keep `VIDEO_SHOTLIST_2MIN.md` only as the pacing baseline

## Fixed Demo Facts

These points should stay word-for-word consistent across PPT, video, poster, and defense:

1. The strongest feature is not generic generation, but evidence-backed `ask`.
2. The live path already verified under the real runtime is:
   - `upload -> ask -> citation -> PDF -> refusal`
3. The locked candidate question set is:
   - `这篇论文主要研究了什么问题？`
   - `作者最终的方法排名和总体准确率分别是多少？`
   - `木星有几颗卫星？`
4. The current QA decision is:
   - default QA: `deepseek-v4-flash` (V6 contract-patch holdout default; `qwen3-235b-a22b-instruct-2507` is the rollback fallback; `qwen3-32b` remains historical validated fallback)
   - summary / outline remain on `qwen3-235b-a22b-instruct-2507` (not re-evaluated, so no switch)
5. The gold-sample comparison result is:
   - both `qwen3-235b-a22b-instruct-2507` and `qwen3-32b` passed `2 answerable + 1 refusal` on the locked sample
   - that comparison is historical evidence the platform path works; the current default QA was selected separately via V6 holdout

## PPT Mapping

### Slide 1: Problem + Positioning

- Problem:
  - long documents are slow to read
  - generic chat tools answer without verifiable grounding
- Positioning:
  - a document assistant for paper/report reading and defense preparation
  - every answer can jump back to PDF evidence

Suggested assets:

- `PROJECT_ONE_PAGER.md`
- opening sentence from `DEMO_SCRIPT_3MIN.md`

### Slide 2: System Path

- Show the shortest verified path:
  - upload
  - ask
  - citation
  - PDF
  - refusal

Suggested assets:

- `ARCHITECTURE.md`
- `gold_sample_replay_real_summary_latest.md`

### Slide 3: Answerable Ask

- Screenshot:
  - `20260419_gold_ask_research_focus.png`
- Talking point:
  - the answer appears together with citations and evidence snippets
  - this is not a chat shell response detached from the document

### Slide 4: PDF Evidence Render

- Screenshot:
  - `20260419_gold_pdf_render.png`
- Talking point:
  - the system can jump back into the cited PDF page
  - evidence is shown visually, not only as a page number

### Slide 5: Second Answerable Ask + Model Decision

- Screenshot:
  - `20260419_gold_ask_rank_accuracy.png`
- Talking point:
  - the system can return concrete numeric answers with citations
  - both tested QA models pass, but `235b` remains the primary choice

Suggested supporting artifacts:

- `gold_sample_qa_compare_latest.md`

### Slide 6: Refusal

- Screenshot:
  - `20260419_gold_refusal.png`
- Talking point:
  - if the ask is off-topic, the system refuses instead of fabricating
  - this keeps the demo focused on evidence-backed answers, not generic chat

## Video Mapping

- The 2-minute path should stay:
  - open the locked sample
  - ask Q1
  - open citation and PDF
  - ask Q2
  - ask refusal
- Use:
  - `VIDEO_SHOTLIST_2MIN.md`
  - `video_subtitles.srt`
  - `VIDEO_SHOTLIST_5MIN_FINAL.md`
  - `video_subtitles_5min_final.srt`

## Poster Mapping

- Keep the center story simple:
  - why generic document chat is not enough
  - how evidence-backed ask works
  - one answerable example
  - one refusal example
- Use:
  - `POSTER_COPY.md`
  - `poster.html`
  - `poster.pdf`

## Defense Notes

- Use `FINAL_SUBMISSION_CHECKLIST.md` as the final freeze sheet.
- Use `DEFENSE_DEMO_RISK_CHECKLIST.md` as the live operator sheet.
- Do not over-sell `summary` / `outline` as having the same evidence semantics as `ask`.
- Do not center login/invite-code flow in the product story.
- Do not use broader replay artifacts as the main judging evidence unless specifically asked.
- If asked about stability, cite the locked gold-sample reports first, then mention broader replay as secondary coverage.
