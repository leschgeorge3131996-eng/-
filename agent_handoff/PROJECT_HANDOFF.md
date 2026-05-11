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
- Current primary/fallback decision (snapshot 2026-04-18, superseded — see 2026-04-30 entry below):
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
  - `evidence/exports/competition_asset_pack_20260420_173101/`

## 2026-04-20 External Review Pack Refresh

- Root review docs now exist for direct handoff to another AI:
  - `PROJECT_CONTEXT.md`
  - `REVIEW_PROMPT.md`
  - `REVIEW_BUNDLE_INDEX.md`
- `scripts/export_review_bundle.ps1` now packages the current strict `G3` evidence, current judged-asset baselines, and current whole-project review context instead of the older warm-state framing
- Latest external review artifacts:
  - `review_bundle_stage_20260420_141123/`
  - `review_bundle_20260420_141123_final_competition_review.zip`
- Older `review_bundle_*.zip` archives were removed locally; old `review_bundle_stage_*` directories remain as readable history

## 2026-04-20 Review-Driven Final-Material Cleanup

- The old `6`-slide / `2`-minute materials were not deleted, but they were demoted from primary-entry status in the highest-visibility material docs:
  - `evidence/materials/MATERIALS_INDEX.md`
  - `evidence/materials/PRODUCT_TECHNICAL_WRITEUP.md`
- The explicit primary judged-material path is now:
  - `PPT_DECK_3PAGES_FINAL.md`
  - `VIDEO_SHOTLIST_5MIN_FINAL.md`
  - `deliverables/competition_kit/deck_3page_final.pdf`
  - `deliverables/competition_kit/video_subtitles_5min_final.srt`
- Provider residue was also removed from the live error wording in:
  - `backend/app/services/model_client.py`

## 2026-04-20 Final Submission / Defense Control Sheets

## 2026-04-21 Quantitative Evaluation Metrics

## 2026-04-21 Frontend UX Polish

- Evidence confidence bar added to ask results:
  - three-dot signal indicator: green (declared) / orange (candidate) / red (none)
  - shows citation count and quote count inline
  - file: `frontend/src/components/ResultPanel.tsx`
- Citation card is now fully clickable for PDF jump:
  - entire card wraps a button when PDF preview is available
  - hover shows "→ 跳转 PDF" hint via existing `.citation-button::after`
- Refusal result now renders a dedicated card instead of plain warning text:
  - red-bordered card with "检索无命中，拒绝回答" heading
  - explains retrieval-gate interception without model call
  - `data-testid="refusal-card"` for test targeting
- Drag-and-drop upload zone replaces plain file input:
  - dashed border highlights on drag-over
  - click still opens file picker
  - shows selected filename or placeholder hint
- Hero button ("填充示例文档") now pulses like the submit button
- All 7 frontend smoke tests still pass; build clean

- A new evaluation script now exists:
  - `scripts/compute_eval_metrics.py`
- It reads the `9` strict G3 request entries from `data/logs/call_logs.jsonl` and computes `8` quantitative metrics
- Output report:
  - `evidence/reports/quantitative_eval_metrics.md`
- Key numbers (strict G3, `3` runs × `3` prompts):
  - evidence declaration rate: `100%`
  - citation page accuracy: `100%`
  - retrieval page coverage: `100%`
  - evidence quote rate: `100%`
  - chunk utilization: `38%`
  - refusal precision: `100%`
  - cross-run consistency: `100%`
  - avg answerable latency: `5521 ms`
- These numbers were also written into:
  - `evidence/materials/HARD_EVIDENCE_SUMMARY.md` (new "量化评测指标" section)
  - `evidence/materials/SCORING_EVIDENCE_MATRIX.md` (技术能力追问答法 updated)
- Practical meaning:
  - judge-facing docs now have concrete numbers instead of only qualitative pass/fail
  - PPT and defense wording can cite specific metrics

## 2026-04-20 Final Submission / Defense Control Sheets

- Two explicit operator-control docs now exist for the last mile:
  - `evidence/materials/FINAL_SUBMISSION_CHECKLIST.md`
  - `evidence/materials/DEFENSE_DEMO_RISK_CHECKLIST.md`
- They were also wired into the primary prep/material/export path:
  - `evidence/materials/SUBMISSION_PREP_GUIDE.md`
  - `evidence/materials/COMPETITION_ASSET_PACK.md`
  - `evidence/materials/MATERIALS_INDEX.md`
  - `scripts/export_competition_asset_pack.ps1`
  - `scripts/export_review_bundle.ps1`
- Practical meaning:
  - final native `PPT` and final edited `5`-minute video now have a single freeze-control sheet
  - judged-demo warmup, fallback, and anti-overclaim rules now have a single live operator sheet
  - this does not reopen scope; it narrows execution around the current strongest judged path
- Latest export verification after wiring these docs:
  - `powershell -ExecutionPolicy Bypass -File .\scripts\export_competition_asset_pack.ps1`
  - `evidence/exports/competition_asset_pack_20260420_173101/`
  - `PACK_CONTENTS.md` confirms both:
    - `FINAL_SUBMISSION_CHECKLIST.md`
    - `DEFENSE_DEMO_RISK_CHECKLIST.md`

## 2026-04-30 Default QA Switch (post V6 contract-patch holdout)

- After the V6 extreme-full + contract-patch reruns, `MODEL_QA` was deliberately switched from `qwen3-235b-a22b-instruct-2507` to `deepseek-v4-flash`:
  - V6 contract-patch holdout: `deepseek-v4-flash` `71 / 72` vs `qwen3-235b-a22b-instruct-2507` `56 / 72`
  - report: `evidence/reports/holdout_eval_v6_contract_patch_qwen_vs_flash_20260430.md`
  - the switch then passed `scripts/predeploy_sanity.py` at `3 / 3` gold and `11 / 11` gates as READY
- Current runtime defaults (matches `.env`):
  - `MODEL_QA=deepseek-v4-flash`
  - `MODEL_SUMMARY=qwen3-235b-a22b-instruct-2507`
  - `MODEL_OUTLINE=qwen3-235b-a22b-instruct-2507`
- Rollback fallback for QA: `qwen3-235b-a22b-instruct-2507` — this is also the model the locked gold-sample `3 / 3` and the strict G3 6-run batch were originally run against, so it remains a trusted recovery path if the deploy environment behaves unexpectedly
- Practical implication for judges/defense:
  - "current default QA model" answer in any answer line should now be `deepseek-v4-flash`
  - "已验证 fallback" is `qwen3-235b-a22b-instruct-2507`, not `qwen3-32b` (`qwen3-32b` is historical gold-sample fallback only)
  - the historical `qwen3-235b` `3 / 3` and `qwen3-32b` `3 / 3` numbers in gold-sample compare are still real and still cited as evidence that the platform path works — they were the comparison that locked the gold sample, not the V6 default-selection decision
- The earlier 2026-04-18 / 2026-04-24 lines that said "keep `qwen3-235b-a22b-instruct-2507` as default" are 2026-04-18 / 2026-04-24 snapshots and are now superseded by this entry; they have been demoted in:
  - `agent_handoff/PROJECT_HANDOFF.md` (snapshot note added to the 2026-04-18 entry)
  - `agent_handoff/TECHNICAL_OPTIMIZATION_ROADMAP_20260424.md` (top-of-file update banner)
  - `agent_handoff/FREEZE_FACT_SHEET_20260419.md` (current `MODEL_QA` field switched)
  - the judge-facing materials listed in the next section

## 2026-04-30 Judge-Facing Material Sync

The "current default QA model = ..." fields in the actively used judge-facing materials were synced to match the V6 switch. Historical experiment numbers (gold-sample `3 / 3`, strict G3 batch) were preserved untouched as historical evidence. Files updated:

- `evidence/materials/HARD_EVIDENCE_SUMMARY.md`
- `evidence/materials/PLATFORM_USAGE_EVIDENCE.md`
- `evidence/materials/SCORING_EVIDENCE_MATRIX.md`
- `evidence/materials/PRODUCT_TECHNICAL_WRITEUP.md`
- `evidence/materials/POSTER_COPY.md`
- `evidence/materials/COMPETITION_ASSET_PACK.md`
- `evidence/materials/VIDEO_SHOTLIST_5MIN_FINAL.md`
- `evidence/materials/PPT_DECK_3PAGES_FINAL.md`

Intentionally NOT updated (kept as time-stamped baselines or historical experiment records):

- `evidence/materials/PPT_DECK_6SLIDES.md` (already demoted to baseline-only in `MATERIALS_INDEX.md`)
- `evidence/materials/VIDEO_SHOTLIST_2MIN.md` (already demoted to baseline-only)
- `evidence/materials/STRICT_G3_EXECUTION_PLAN.md` (G3 was actually run on `qwen3-235b-a22b-instruct-2507`; that is historical fact, not a current-state claim)
- `evidence/materials/HOLDOUT_EVAL_V3_20260429.json` (a V3 holdout description; historical experiment record)
- `agent_handoff/MODEL_STRATEGY_EXTREME_PLAN_20260429.md` (the plan that ran the V5/V6 holdouts in the first place; its "stable current default" line is the starting state of that plan)

## 2026-05-09 UX Cleanup Pass

- Stripped the demo-jargon vocabulary that had been accumulating on user-facing surfaces:
  - removed `精简速读兜底` preset (button + prompt + load/timeout copy + test)
  - demo task cards now seed the sample document automatically when none is loaded and scroll to the task input
  - default task type flipped `summary` → `ask` so the first thing a visitor lands on is evidence-back-linked QA
  - `一键演示入口` → `快速体验`; `推荐追问 1/2` / `拒答边界` chips now display the actual question; `示例摘要/问答/提纲` → `试一试 摘要/问答/提纲`
  - `演示模式/演示环境/演示会话` → `试用模式/试用环境/试用会话`
  - sample doc renamed `demo_research_brief.md` → `sample_brief.md`
  - `论文速读工作台` → `论文速读` (kicker, button, prompt, ResultPanel detection — kept backward-compatible)
- Hero flow strip is now stage-aware: it tracks `loadStage` (uploading → 1+2 brand-accent; model → 3 solid, 4 pulsing; idle+result → soft-green done state); idle keeps the breathing animation
- Upload-zone 状态卡 folded into a session chip beside the panel title plus a one-line dropzone footnote
- Demo session bootstrap silently retries twice (800ms each) before surfacing an auth-error card, so first-time visitors no longer see a red error on a transient cold start
- Commit: `d4b1923` "Strip demo-jargon UI and wire the hero flow to real load stage"
- Guiding principle captured in memory `feedback_user_first.md`: real-user lens beats judge-lens; demo scaffolding should not bleed into the main UI vocabulary

## 2026-05-10 Token Compression Evidence (Scoring Add-On #4)

- Competition rubric confirmed from 赛题 PDF (`2026第二十一届研电赛赛题指南及清单.pdf`, p.117-118, 无问芯穹赛题一):
  - main: `平台使用 20` + `产品能力 40` + `技术能力 40`
  - 4 × 5-point add-ons: `平台利用率`, `商业化潜力`, `大模型与智能体能力`, **`Token 消耗量`** (either high per-task consumption OR compression technique)
- Preprocessing pipeline (`DocumentParser → ChunkService → ContextPlannerService`) fits the compression branch; evaluation script made it quantitative:
  - `scripts/eval_token_compression.py`: walks 10 sample docs (8 short md/txt + 2 long PDFs) × 3 task types through the real services, counts tokens with tiktoken `cl100k_base`, compares `ContextPlannerService.plan().document_text` against "raw_text as prompt" baseline
  - `no_match` refusal-path samples explicitly excluded from headline averages (per `project_eval_honesty`)
- Numbers (32 task samples total):
  - long-doc ask: 4 samples, avg **89.1%** saved, peak **93.1%** (Attention paper `10,263 → 704` tokens)
  - long-doc summary/outline: avg 83.3%
  - long-doc overall: 86.2%
  - short-doc overall: -4.2% (honestly flagged as non-target scenario; single-chunk docs get a few wrapper tokens from page/heading markers)
- Materials synced:
  - `evidence/reports/token_compression_eval.md` + `.json` (canonical)
  - `evidence/materials/HARD_EVIDENCE_SUMMARY.md` new section 8
  - `evidence/materials/SCORING_EVIDENCE_MATRIX.md` new "加分项" table + dedicated follow-up Q&A
  - `agent_handoff/TASK_BOARD.md` now line-item for the add-on
- Commit `943b714`, pushed to `origin/master` together with the 2026-05-09 UX pass
- Tool note: `tiktoken==0.12.0` installed into `.venv` for this evaluator only; main runtime still relies on provider-side `token_in` from `call_logs.jsonl` for real-call truth

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

1. Token compression scoring add-on #4 is now closed with evidence — reuse `evidence/reports/token_compression_eval.md` + `HARD_EVIDENCE_SUMMARY.md` §8 verbatim in rehearsal; do not re-run unless the pipeline changes
2. Start from `evidence/exports/competition_asset_pack_20260419_211551/`
3. Use the latest final external-review bundle for one more targeted judging-risk review:
   - `review_bundle_stage_20260419_211551/`
   - `review_bundle_20260419_211551_final_competition_review.zip`
   - this version adds `PROJECT_CONTEXT.md`, so another AI sees the project background, target, and scope constraints before judging the current state
4. Treat `G3` as closed for the current strict fresh-upload judged-demo path; do not reopen Q2 or G3 as default blockers unless the final environment changes or new contrary evidence appears
5. Keep runtime/docs/materials aligned to `Wuwen Xinqiong` + the current primary `MODEL_QA` decision
6. Finalize judged-demo materials and spoken defense wording before doing any new feature work

### Layout / visual guardrails (important for next operator)

- Warm cream + ember-orange theme is the user-approved aesthetic baseline — do not bulk-swap to "corporate blue / document grey" no matter what external design tools recommend (`feedback_aesthetic`)
- When changing the workspace layout, the answer (ResultPanel) must not move further down the page than its current position; "left controls + answer stacked / right PDF" is explicitly rejected (`feedback_layout_answer_position`)
- Demo scaffolding vocabulary (`演示 / 白名单 / 兜底 / 拒答边界 / 推荐追问 1/2`) has been stripped from user-facing surfaces; keep it that way (`feedback_user_first`)

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
