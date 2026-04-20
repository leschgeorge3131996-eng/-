# Project Handoff

## Identity

- Project: `YanDatong` / `Yandatong`
- Type: document workbench prototype
- Best current positioning:
  - a document assistant for paper/report reading and defense preparation
  - strongest differentiator is evidence back-linking rather than general-purpose generation
- Release posture:
  - controlled alpha
  - not public open SaaS

## 2026-04-18 Runtime Update

- Current active provider/runtime is now `Wuwen Xinqiong`
- Current default interface:
  - `https://cloud.infini-ai.com/maas/v1/chat/completions`
- Current primary/fallback decision:
  - primary: `qwen3-235b-a22b-instruct-2507`
  - fallback candidate: `qwen3-32b`
- Real in-project minimal path now verified on:
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
- Verified path:
  - `upload -> ask -> citation -> PDF -> refusal`
- Current caution:
  - refusal demos should use a purely off-topic question; prompts that still mention document entities may retrieve and answer
- Current gold-sample candidate:
  - document: `evidence/samples/chinese_llm_spatial_eval.pdf`
  - prompts:
    - `这篇论文主要研究了什么问题？`
    - `作者最终的方法排名和总体准确率分别是多少？`
    - `木星有几颗卫星？`
- Authoritative prompt identifiers for fresh artifacts:
  - `askResearchFocus`
  - `askRankAccuracy`
  - `refusal`
- If another doc still shows mojibake prompt text, treat that as a stale text artifact and use the prompt identifiers above.
- Current QA comparison artifact:
  - `evidence/reports/gold_sample_qa_compare_latest.md`
- Current gold-sample replay artifact:
  - `evidence/reports/gold_sample_replay_real_latest.md`
- Current QA decision:
  - keep `qwen3-235b-a22b-instruct-2507` as primary
  - keep `qwen3-32b` as validated fallback

## Current Verified State

As of `2026-04-18`:

- backend tests: `55 passed`
- frontend smoke tests: `7 passed`
- frontend build: passed
- real provider (`Wuwen Xinqiong`) minimal path:
  - answerable `ask`: passed with citations
  - cited PDF page fetch/render: passed
  - true off-topic refusal: passed
- gold-sample candidate QA comparison:
  - `qwen3-235b-a22b-instruct-2507`: `3/3` passed
  - `qwen3-32b`: `3/3` passed
- gold-sample real replay:
  - `2 answered + 1 refused`
  - `0 errors`
  - current replay tooling now reflects the cookie/session + document-token runtime posture
- gold-sample screenshot refresh:
  - `evidence/screenshots/20260419_gold_ask_research_focus.png`
  - `evidence/screenshots/20260419_gold_pdf_render.png`
  - `evidence/screenshots/20260419_gold_ask_rank_accuracy.png`
  - `evidence/screenshots/20260419_gold_refusal.png`
  - `evidence/screenshots/20260419_stats_panel.png`
  - `evidence/screenshots/20260419_api_docs.png`
  - metadata sidecars:
    - `20260419_gold_ask_research_focus.json`
    - `20260419_gold_pdf_render.json`
    - `20260419_gold_ask_rank_accuracy.json`
    - `20260419_gold_refusal.json`
- competition drafting assets:
  - `evidence/materials/PPT_DECK_3PAGES_FINAL.md`
  - `evidence/materials/VIDEO_SHOTLIST_5MIN_FINAL.md`
  - `evidence/materials/PPT_DECK_6SLIDES.md`
  - `evidence/materials/VIDEO_SHOTLIST_2MIN.md`
  - `evidence/materials/POSTER_COPY.md`
  - `scripts/export_competition_asset_pack.ps1`
- printable visual prototypes:
  - `deliverables/competition_kit/deck.html`
  - `deliverables/competition_kit/poster.html`
- PDF export helper:
  - `scripts/export_competition_pdfs.js`
- current exported PDFs:
  - `deliverables/competition_kit/deck.pdf`
  - `deliverables/competition_kit/poster.pdf`
- asset-bundle export now includes:
  - `deliverables/competition_kit/*`
  - `scripts/export_competition_pdfs.js`
- video subtitle baseline:
  - `deliverables/competition_kit/video_subtitles.srt`
- fresh Q2 stability check:
  - `evidence/experiments/20260419_q2_declared_stability_check.md`
  - `3 / 3` fresh local real runs returned:
    - `evidence_mode=declared`
    - `used_chunk_count=2`
    - `evidence_quote_count=2`
    - `citation_count=2`
    - answer: `作者最终的方法排名第六，总体准确率为56.20%。`
- `G3` rehearsal record:
  - `evidence/experiments/20260420_g3_strict_rehearsal.md`
  - current status: `pass (strict fresh-upload three-run batch)`
  - caveat:
    - this is locked-path reproducibility evidence, not open-domain generalization proof
    - the PDF click/render step is part of the live checklist, while the repo-verifiable portion is the request-id/timestamp trace

Main verification commands:

```powershell
.venv\Scripts\python.exe -m pytest backend\tests
cd frontend
npm test
npm run build
```

Operator rehearsal result:

- `G1`: pass
- `G2`: pass
- `G3`: pass (strict fresh-upload three-run batch)
- authoritative freeze-fact reference:
  - `agent_handoff/FREEZE_FACT_SHEET_20260419.md`

## 2026-04-19 Final Sweep

- `DEMO_SCRIPT_3MIN.md` now follows the real judged-demo path instead of the old "homepage sample entry loads the locked PDF" wording
- `QA_BRIEF.md` now includes fixed spoken answers for:
  - strict `G3`
  - pure off-topic refusal wording
  - `summary / outline` de-emphasis
- screenshot sidecars now use ASCII-safe provenance keys:
  - `prompt_id`
  - `source_prompt_id`
  - `preview_page`
  - `pdf_status_present`
  - `evidence_snippet_present`
- latest production bundle:
  - `evidence/exports/competition_asset_pack_20260419_211551/`
- latest external review bundle:
  - `review_bundle_stage_20260419_211551/`
  - `review_bundle_20260419_211551_final_competition_review.zip`

## 2026-04-20 Submission-Source Upgrade

- Official source drafts now exist for the remaining judged assets:
  - `evidence/materials/PPT_DECK_3PAGES_FINAL.md`
  - `evidence/materials/VIDEO_SHOTLIST_5MIN_FINAL.md`
- The old `6`-slide / `2`-minute files remain baselines only:
  - `PPT_DECK_6SLIDES.md`
  - `VIDEO_SHOTLIST_2MIN.md`
- Export packaging now includes the new final-source drafts:
  - `scripts/export_competition_asset_pack.ps1`
- Export packaging was also re-run successfully after the update:
  - `evidence/exports/competition_asset_pack_20260420_125210/`
  - `PACK_CONTENTS.md` in that folder confirms both final-source drafts are included

## 2026-04-20 Repo-Native Final Asset Baselines

- Repo-native judged-deck outputs now exist:
  - `deliverables/competition_kit/deck_3page_final.html`
  - `deliverables/competition_kit/deck_3page_final.pdf`
- Repo-native judged-video timing baseline now exists:
  - `deliverables/competition_kit/video_subtitles_5min_final.srt`
- `scripts/export_competition_pdfs.js` now exports and sanity-checks:
  - `deck_3page_final.pdf` -> `3` pages
  - `deck.pdf` -> `6` pages
  - `poster.pdf` -> `1` page
- Latest local handoff pack after these additions:
  - `evidence/exports/competition_asset_pack_20260420_135135/`

## What Was Added In The Latest Iterations

### Evidence and PDF chain

- `ask` evidence semantics were separated into:
  - declared evidence
  - candidate context
  - none
- frontend now exposes `evidence_mode`
- PDF preview matching now distinguishes:
  - `exact_match`
  - `fragment_match`
  - `not_found`
  - `no_snippet`
- PDF snippet matching is now page-specific instead of one-snippet-for-all-pages

### Document lifecycle

- per-document `access_token`
- document retention metadata
- delete current document flow
- expired document cleanup script

### Frontend stability

- key smoke tests added for:
  - login
  - upload -> summary
  - ask -> citation -> PDF preview
  - recent result restore
  - delete current document
  - logout
  - stale local auth state recovery

### Trial boundary and ownership

- invite-code trial session support
- session-backed document ownership
- file/task/log access requires a valid session
- document access still also requires document-level access token

### Session hardening

- session moved to `HttpOnly` cookie
- frontend no longer stores `session_token`
- backend no longer accepts `X-Session-Token` fallback
- cookie is now the only session entry

## Important Product Truths

These points should stay stable unless the user explicitly changes direction:

1. The strongest feature is evidence-backed `ask`
2. `summary` and `outline` are useful, but they are still weaker in grounding semantics than `ask`
3. Login / invite code exists to enforce a controlled-alpha boundary, but `DEMO_MODE=true` can bypass it for judging/demo flow
4. Login / invite code should not be presented as a product feature
5. Public-SaaS framing is currently too broad and should be avoided

## Demo And Judging Guidance

If the next operator is preparing for review, judging, or defense:

- emphasize:
  - upload -> parse -> retrieve -> answer -> return to evidence
  - PDF evidence preview
  - structured evidence / citation behavior
- de-emphasize:
  - generic platform framing
  - auth as a feature
  - broad SaaS language
- be careful with:
  - the current stats panel if it shows noisy latency/error numbers
  - long interaction paths before the first impressive result

Best short demo path:

1. enter app
2. use the locked gold-sample candidate or the corresponding demo document
3. run the primary answerable `ask`
4. open citation
5. show the cited PDF render / evidence highlight
6. run the off-topic refusal prompt

## Architecture Map

### Backend

Main files:

- `backend/app/main.py`
- `backend/app/api/routes.py`
- `backend/app/core/config.py`
- `backend/app/core/exceptions.py`
- `backend/app/schemas/auth.py`
- `backend/app/schemas/document.py`
- `backend/app/schemas/task.py`
- `backend/app/services/auth_service.py`
- `backend/app/services/file_service.py`
- `backend/app/services/context_planner.py`
- `backend/app/services/model_client.py`
- `backend/app/services/task_service.py`
- `backend/app/services/retrieval_service.py`

Key responsibilities:

- `routes.py`: API wiring and cookie/session boundary
- `auth_service.py`: invite-code sessions and session record lifecycle
- `file_service.py`: upload persistence, parsed outputs, ownership checks, document deletion
- `context_planner.py`: task-specific chunk/context selection
- `model_client.py`: provider integration and prompting
- `task_service.py`: retrieval, evidence validation, response assembly, logging/cache interplay
  - latest note: `ask` now performs a one-step internal retry when structured evidence is missing, and logs `ask_evidence_retry_count`

### Frontend

Main files:

- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/components/ResultPanel.tsx`
- `frontend/src/components/PdfPreviewPanel.tsx`
- `frontend/src/App.smoke.test.tsx`
- `scripts/capture_gold_sample_screenshots.js`
- `evidence/materials/COMPETITION_ASSET_PACK.md`

Key responsibilities:

- `App.tsx`: top-level session flow, upload/task flow, history restore, preview state
- `api.ts`: cookie-backed requests and document-token URL building
- `ResultPanel.tsx`: output rendering, evidence/source display, export behavior
- `PdfPreviewPanel.tsx`: rendered PDF-page preview with evidence-highlight overlays

Main demo path should now be treated as:

- `ask -> citation -> PDF render -> refusal`

## Environment And Runtime Notes

- Local environment uses Windows PowerShell
- Repo path during recent work:
  - `C:\Users\Administrator\Desktop\project`
- Session cookie config is now in `.env.example`:
  - `SESSION_COOKIE_NAME`
  - `SESSION_COOKIE_SECURE`
  - `SESSION_COOKIE_SAMESITE`
- For true cross-site deployment, cookie settings may need:
  - `SESSION_COOKIE_SECURE=true`
  - `SESSION_COOKIE_SAMESITE=none`

## Current Open Priorities

These are the best next steps if work continues:

### Highest value for judging/demo

1. Start from `evidence/exports/competition_asset_pack_20260419_211551/`
2. Use the latest final external-review bundle for one more targeted judging-risk review:
   - `review_bundle_stage_20260419_211551/`
   - `review_bundle_20260419_211551_final_competition_review.zip`
   - this version adds `PROJECT_CONTEXT.md`, so another AI sees the project background, target, and scope constraints before judging the current state
3. Treat `G3` as closed for the current strict fresh-upload judged-demo path; do not reopen Q2 or G3 as default blockers unless the final environment changes or new contrary evidence appears
4. Keep runtime/docs/materials aligned to `Wuwen Xinqiong` + the current primary `MODEL_QA` decision
5. Finalize judged-demo materials and spoken defense wording before doing any new feature work

### Highest value for broader external testing

1. Add a dedicated expired-session cleanup script
2. Add CSRF / origin validation for cookie-backed state-changing routes

### Good but not urgent

1. Broader sample-set replay refresh as secondary coverage
2. Stronger grounding semantics for `summary` / `outline`

## Explicit Non-Priorities

Do not expand into these unless the user explicitly asks:

- new task types
- OCR-first pipeline
- local model branch
- major visual redesign
- public open trial framing

## Dirty Worktree Note

The repo may still be in a dirty state between sessions, and that is expected.

Recent uncommitted work is more likely to be:

- doc/material alignment around the locked gold-sample path
- external-review or external-strategy bundle files
- temporary replay artifacts that should not be committed by default

Always run:

```powershell
git status --short
```

before making assumptions.

## External Review Artifacts

Recent external review / strategy bundle files may include:

- `REVIEW_BUNDLE_INDEX.md`
- `REVIEW_PROMPT.md`
- `EXTERNAL_AI_STRATEGY_BRIEF.md`
- `EXTERNAL_AI_STRATEGY_BUNDLE_INDEX.md`
- `EXTERNAL_AI_STRATEGY_PROMPT.md`
- `review_bundle_stage_20260416_231332.zip`
- `review_bundle_stage_*`
- `review_bundle_*_final_competition_review.zip`

These are useful for third-party model review, but they are not the canonical long-term handoff source.
