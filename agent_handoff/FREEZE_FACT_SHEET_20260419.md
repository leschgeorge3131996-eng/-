# Freeze Fact Sheet (`2026-04-19`)

> Last refreshed: `2026-04-27`. The filename is kept for cross-reference stability; the body has been updated to reflect work landed between `2026-04-20` and `2026-04-25`.

Use this file as the quickest authoritative reference when another operator or another AI needs the current judged-demo status without re-reading all historical notes.

## Main Story

- Keep the judged-demo story fixed to:
  - `upload -> ask -> citation -> PDF -> refusal`
- Do **not** present `login` / invite flow as a product capability
- Do **not** expand scope back into generic chat / SaaS framing
- Strongest differentiator remains evidence back-linking, not generic generation

## Locked Demo Inputs

- Locked sample:
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
- Locked prompt triad:
  - `这篇论文主要研究了什么问题？`
  - `作者最终的方法排名和总体准确率分别是多少？`
  - `木星有几颗卫星？`

- Authoritative prompt identifiers for all fresh screenshot/report artifacts:
  - `askResearchFocus`
  - `askRankAccuracy`
  - `refusal`
- If an older file still shows mojibake prompt literals, treat that as a historical text artifact and use the prompt identifiers above.
- Exact wording source of truth:
  - `evidence/materials/COMPETITION_ASSET_PACK.md`

## Runtime Facts

- Current active provider path:
  - `Wuwen Xinqiong` (`https://cloud.infini-ai.com/maas/v1/chat/completions`)
- Current default `MODEL_QA`:
  - `deepseek-v4-flash` (switched after the V6 contract-patch holdout — see `evidence/reports/holdout_eval_v6_contract_patch_qwen_vs_flash_20260430.md`, `71 / 72` vs `56 / 72` for `qwen3-235b-a22b-instruct-2507`)
- Current rollback `MODEL_QA` fallback:
  - `qwen3-235b-a22b-instruct-2507` (this is also the model the gold-sample `3 / 3` and strict G3 batches were run on; trusted recovery path)
- Current `MODEL_SUMMARY` / `MODEL_OUTLINE`:
  - `qwen3-235b-a22b-instruct-2507` (not re-evaluated in V6; keep until separately retested)
- Validated fast fallback (test-switch only if live latency is the blocker):
  - `qwen3-next-80b-a3b-instruct`
- Historical gold-sample fallback (kept for completeness, not the preferred fallback):
  - `qwen3-32b`
- Demo-mode bypass:
  - set `DEMO_MODE=true` on the deploy URL so judges do not see the invite/login boundary

## Verification Facts (current HEAD)

- Frontend tests:
  - `npm test -- --run` -> `13 passed`
- Frontend build:
  - `npm run build` -> passed (Vite still warns about the existing large chunk; not a regression)
- Backend tests:
  - `.venv\Scripts\python.exe -m pytest backend\tests` -> `67 passed`
- Q2 fresh evidence check:
  - `evidence/experiments/20260419_q2_declared_stability_check.md`
  - result: `3 / 3` fresh local runs returned `declared`

## Gate Wording

- `G1`: pass
- `G2`: pass
- `G3`: pass for the current **strict fresh-upload six-run** path
  - first batch (`2026-04-19`): `13.5s`, `12.9s`, `15.8s`
  - continuation (`2026-04-21`, recorded `2026-04-23`): `8.0s`, `31.3s`, `63.5s`
  - all 6 runs used fresh `file_id`, `cache_hit=false`, no fallback; full 18 request IDs (`6 runs × 3 prompts`) are indexed in `evidence/materials/PLATFORM_USAGE_EVIDENCE.md`
- Honest caveat for `G3`:
  - current strongest evidence is still for the locked gold-sample judged-demo path, not open-domain product generalization
  - if the final target environment changes, treat screenshot refresh / final dry-run as asset work rather than reopening the engineering chain

## Quantitative Evaluation Facts

- Three-layer evaluation story (do not collapse into a single number):
  1. historical `46/51` exposed retrieval boundaries
  2. model-selection replay chose default at `48/51` (`evidence/reports/model_selection_evaluation_20260424.md`)
  3. final default-model retrieval/context patch closed the suite at `51/51` (`evidence/reports/extended_eval_v1_qwen3_235b_a22b_instruct_2507_retrieval_patch.md`)
- Strict-G3 quantitative metrics (`evidence/reports/quantitative_eval_metrics.md`):
  - evidence declaration rate: `100%`
  - citation page accuracy: `100%`
  - retrieval page coverage: `100%`
  - evidence quote rate: `100%`
  - chunk utilization: `38%`
  - refusal precision: `100%`
  - cross-run consistency: `100%`
  - avg answerable latency: `5521 ms`
- Wording rule:
  - citation/page-hit/declaration are final metrics on the locked path
  - verbatim quote validation applies when the model provides quote text; do **not** claim every answer has a verbatim quote or open-domain `100%`

## Material Freeze Facts

- Primary judged-material entry now points to the `3`-page / `5`-minute final path (older `6`-slide / `2`-minute baselines were demoted, not deleted):
  - `evidence/materials/PPT_DECK_3PAGES_FINAL.md`
  - `evidence/materials/VIDEO_SHOTLIST_5MIN_FINAL.md`
  - `deliverables/competition_kit/deck_3page_final.html`
  - `deliverables/competition_kit/deck_3page_final.pdf` (`3` pages, sanity-checked)
  - `deliverables/competition_kit/video_subtitles_5min_final.srt`
- Older baselines kept for reference only:
  - `evidence/materials/PPT_DECK_6SLIDES.md` -> `deliverables/competition_kit/deck.pdf` (`6` pages)
  - `evidence/materials/VIDEO_SHOTLIST_2MIN.md` -> `deliverables/competition_kit/video_subtitles.srt`
  - `evidence/materials/POSTER_COPY.md` -> `deliverables/competition_kit/poster.pdf` (`1` page)
- PDF export now has sanity checks in:
  - `scripts/export_competition_pdfs.js`

## Demo Hardening Facts (landed since `2026-04-21`)

- Frontend UX polish:
  - evidence confidence bar (declared/candidate/none indicator)
  - citation card is fully clickable for PDF jump
  - dedicated refusal card replaces plain warning text
  - drag-and-drop upload zone
- Refusal escape:
  - `ask` prompt returns `refused=true` on out-of-scope; `TaskService` honors it via a dedicated `llm_refused` branch
  - extended-eval refusal precision moved from `0%` to `100%`
- Retrieval safety nets:
  - metadata-intent fallback pins first-page chunk for author/affiliation/contribution/name queries
  - parameter/table-like queries get query expansion + neighboring chunks
  - contribution questions append document-head chunks
  - matched-retrieval self-refusals get one stricter retry before accepting `llm_refused`
- Demo-day operator features:
  - `论文速读工作台` preset (one-click structured paper-reading prompt with follow-up chips)
  - `国一演示路线` button (prepares sample doc + digest task in one click, plus whitelisted demo questions)
  - `精简速读兜底` preset (concise digest fallback for slow model/network)
  - frontend task `90s` `AbortController` timeout with operator-friendly fallback wording
  - `重试当前任务` action on task failure that reuses uploaded metadata instead of re-uploading
- Pre-demo gating:
  - `scripts/predeploy_sanity.py` is now a full pre-demo risk light: gold cases plus runtime config, writable data dirs, gold PDF presence, parsed metadata, page text fetch, citation presence, PDF page render, and recent log summary; exit `0` only when every gate passes

## Latest Judge-Facing Evidence Set

- Screenshots:
  - `evidence/screenshots/20260419_gold_ask_research_focus.png`
  - `evidence/screenshots/20260419_gold_pdf_render.png`
  - `evidence/screenshots/20260419_gold_ask_rank_accuracy.png`
  - `evidence/screenshots/20260419_gold_refusal.png`
- Sidecars now exist for:
  - `20260419_gold_ask_research_focus.json`
  - `20260419_gold_pdf_render.json`
  - `20260419_gold_ask_rank_accuracy.json`
  - `20260419_gold_refusal.json`
- Latest local production handoff bundle:
  - `evidence/exports/competition_asset_pack_20260427_213711/`
  - now also carries `FINAL_SUBMISSION_CHECKLIST.md` and `DEFENSE_DEMO_RISK_CHECKLIST.md`
- Latest external final-review bundle (preferred when handing to another AI):
  - `review_bundle_stage_20260427_213721/`
  - `review_bundle_20260427_213721_final_competition_review.zip`
  - root review docs in-repo:
    - `PROJECT_CONTEXT.md`
    - `REVIEW_PROMPT.md`
    - `REVIEW_BUNDLE_INDEX.md`

## Operator Control Sheets

- Final submission freeze sheet:
  - `evidence/materials/FINAL_SUBMISSION_CHECKLIST.md`
- Live judged-demo risk sheet (run before any judged slot):
  - `evidence/materials/DEFENSE_DEMO_RISK_CHECKLIST.md`
- First gate the operator should run `~30 min` before a judged slot:
  - `.venv\Scripts\python.exe scripts\predeploy_sanity.py`
  - it archives `call_logs.jsonl`, runs the 3 gold cases, and emits a single `READY` / `BLOCKED` markdown report

## What Still Matters

1. Keep materials, screenshots, and handoff docs aligned to this fact sheet.
2. If another export bundle is created, ensure it carries the rebuilt `deck/poster` outputs and the two operator-control sheets.
3. If another AI reviews the project, point it first to:
   - `PROJECT_CONTEXT.md`
   - `REVIEW_PROMPT.md`
   - this fact sheet
   so it does not over-index on stale warm-state `G3`, older screenshot prefixes, or pre-rebuild material corruption.
4. Remaining work is **deployment hygiene + rehearsal**, not code:
   - run `scripts/predeploy_sanity.py` on the demo machine until exit `0`
   - confirm `DEMO_MODE=true` is active on the deploy URL
   - record one full-flow fallback video
   - keep devtools closed on the demo machine so judges do not see noisy latency numbers
