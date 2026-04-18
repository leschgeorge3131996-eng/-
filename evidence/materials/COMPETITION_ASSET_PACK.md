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
  - `qwen3-235b-a22b-instruct-2507`
- Validated fallback QA model:
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

- PPT page copy:
  - `evidence/materials/PPT_DECK_6SLIDES.md`
- Video shotlist:
  - `evidence/materials/VIDEO_SHOTLIST_2MIN.md`
- Poster copy:
  - `evidence/materials/POSTER_COPY.md`
- Printable deck/poster prototypes:
  - `deliverables/competition_kit/deck.html`
  - `deliverables/competition_kit/poster.html`
- Current printable PDF baselines:
  - `deliverables/competition_kit/deck.pdf`
  - `deliverables/competition_kit/poster.pdf`
- Video subtitle baseline:
  - `deliverables/competition_kit/video_subtitles.srt`
- One-click export script:
  - `scripts/export_competition_asset_pack.ps1`
- PDF export script:
  - `scripts/export_competition_pdfs.js`

## Fixed Demo Facts

These points should stay word-for-word consistent across PPT, video, poster, and defense:

1. The strongest feature is not generic generation, but evidence-backed `ask`.
2. The live path already verified under the real runtime is:
   - `login -> upload -> ask -> citation -> PDF render -> refusal`
3. The locked candidate question set is:
   - `杩欑瘒璁烘枃涓昏鐮旂┒浜嗕粈涔堥棶棰橈紵`
   - `浣滆€呮渶缁堢殑鏂规硶鎺掑悕鍜屾€讳綋鍑嗙‘鐜囧垎鍒槸澶氬皯锛焋
   - `鏈ㄦ槦鏈夊嚑棰楀崼鏄燂紵`
4. The current QA decision is:
   - keep `qwen3-235b-a22b-instruct-2507` as default
   - keep `qwen3-32b` as validated fallback
5. The comparison result is:
   - both models pass `2 answerable + 1 refusal`
   - `235b` gives slightly richer grounding on the broader question
   - `32b` is slightly faster

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
  - parse
  - retrieve
  - answer
  - open citation
  - render PDF evidence
  - refuse off-topic asks

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
  - the system can stably return concrete numeric answers with citations
  - both tested QA models pass, but `235b` remains the primary choice

Suggested supporting artifacts:

- `gold_sample_qa_compare_latest.md`

### Slide 6: Refusal

- Screenshot:
  - `20260419_gold_refusal.png`
- Talking point:
  - when retrieval does not match, the system refuses instead of fabricating
  - this is part of reliability, not a fallback embarrassment

## Video Mapping

Recommended structure:

1. 0-15s:
   - title + product positioning
2. 15-45s:
   - answerable ask screenshot / live flow
3. 45-65s:
   - PDF render screenshot / citation jump
4. 65-85s:
   - second answerable ask with numeric answer
5. 85-105s:
   - refusal screenshot
6. 105-120s:
   - close with current verification and model decision

Keep the video narration aligned with `DEMO_SCRIPT_3MIN.md`.

## Poster Mapping

Recommended blocks:

1. Problem
   - document reading is slow
   - generic chat tools lack verifiable evidence
2. Method
   - parse
   - chunk
   - retrieve
   - answer
   - jump back to PDF evidence
3. Product demonstration
   - answerable ask screenshot
   - PDF render screenshot
   - refusal screenshot
4. Validation
   - real replay result: `2 answered + 1 refused`
   - QA comparison: `235b` primary, `32b` fallback
5. Conclusion
   - strongest differentiator is evidence-backed document QA

## Asset Checklist

- [ ] `PROJECT_ONE_PAGER.md`
- [ ] `DEMO_SCRIPT_3MIN.md`
- [ ] `ARCHITECTURE.md`
- [ ] `QA_BRIEF.md`
- [ ] `PPT_DECK_6SLIDES.md`
- [ ] `VIDEO_SHOTLIST_2MIN.md`
- [ ] `POSTER_COPY.md`
- [ ] `deliverables/competition_kit/deck.html`
- [ ] `deliverables/competition_kit/poster.html`
- [ ] `deliverables/competition_kit/deck.pdf`
- [ ] `deliverables/competition_kit/poster.pdf`
- [ ] `deliverables/competition_kit/video_subtitles.srt`
- [ ] `gold_sample_qa_compare_latest.md`
- [ ] `gold_sample_replay_real_summary_latest.md`
- [ ] `20260419_gold_ask_research_focus.png`
- [ ] `20260419_gold_pdf_render.png`
- [ ] `20260419_gold_ask_rank_accuracy.png`
- [ ] `20260419_gold_refusal.png`
- [ ] keep `20260419_stats_panel.png` appendix-only; do not place it in the primary six-slide story
- [ ] keep `20260419_api_docs.png` appendix-only; do not place it in the primary six-slide story
- [ ] export a handoff bundle with `scripts/export_competition_asset_pack.ps1`
- [ ] keep `scripts/export_competition_pdfs.js` available for re-export after any visual edits

## Do Not Improvise

- Do not swap the sample document without re-locking the story.
- Do not change the fixed prompt set during judging/demo.
- Do not use the broader sample-set replay as the primary evidence source.
- Do not oversell `summary` / `outline` as having the same grounding semantics as `ask`.
- Do not present auth/demo-mode behavior as a product differentiator.

