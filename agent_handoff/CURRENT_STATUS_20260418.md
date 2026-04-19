# Current Status 2026-04-18

## Execution Baseline

- Active baseline: `agent_handoff/COMPETITION_PLAN_V2.md`
- Future optimization work should follow that plan unless explicitly replaced

## Wuwen Xinqiong Integration

- Default interface verified:
  - `https://cloud.infini-ai.com/maas/v1/chat/completions`
- Current primary model decision:
  - primary: `qwen3-235b-a22b-instruct-2507`
  - fallback: `qwen3-32b`
- External minimal verification completed for both models
- Project-local `.env` is now reading:
  - `MODEL_PROVIDER=infinigence_ai`
  - `USE_MOCK_MODEL=false`
  - `WUQIONG_BASE_URL=https://cloud.infini-ai.com/maas/v1`
  - `MODEL_QA/MODEL_SUMMARY/MODEL_OUTLINE=qwen3-235b-a22b-instruct-2507`

## Project-Internal Verification

- `summary` real call through Wuwen Xinqiong: passed
- `ask` real call through Wuwen Xinqiong: passed
- Returned model during internal verification:
  - `qwen3-235b-a22b-instruct-2507`

## Code Fix Applied

- File changed:
  - `backend/app/services/model_client.py`
- Change:
  - fixed the `ask` prompt template JSON example by escaping inner braces correctly
- Reason:
  - `call_model(task_type='ask', ...)` previously crashed locally with a `ValueError` before any network call
- Result after fix:
  - internal `ask` now returns structured JSON with:
    - `answer`
    - `used_chunk_ids`
    - `evidence_quotes`

## Verification

- Backend tests rerun after the fix:
  - `55 passed`

## Q2 Evidence Stability Fix (`2026-04-19`)

- Trigger:
  - manual demo-mode testing exposed a fresh Q2 regression:
    - prompt: `作者最终的方法排名和总体准确率分别是多少？`
    - symptom: answer text was correct, but `evidence_mode` fell back to `candidate`
    - this still happened after clearing `data/cache`, so it was not just a stale cache artifact
- Code fix applied:
  - `backend/app/services/task_service.py`
    - added a one-step internal retry for `ask` when structured evidence is missing
    - cached/logged `ask_evidence_retry_count` for later debugging
  - `backend/tests/test_services.py`
    - added a regression test covering: first ask response missing JSON evidence -> second ask response declared
- Verification after the fix:
  - backend tests: `55 passed`
  - fresh local real-path check for Q2: `declared`
  - independent fresh stability check:
    - `evidence/experiments/20260419_q2_declared_stability_check.md`
    - `3 / 3` fresh runs returned:
      - `evidence_mode=declared`
      - `used_chunk_count=2`
      - `evidence_quote_count=2`
      - `citation_count=2`
      - answer: `作者最终的方法排名第六，总体准确率为56.20%。`
- Practical meaning:
  - the previously open Q2 blocker for `G3` is now closed at the code/runtime level
  - the remaining `G3` work is process validation, not another known Q2 evidence bug

## G3 Rehearsal Result (`2026-04-19`)

- Operator result:
  - `G3` is now marked `pass`
- Record:
  - `evidence/experiments/20260419_g3_rehearsal_template.md`
- What was verified:
  - `3` consecutive operator runs completed successfully
  - answerable 1 stayed `declared`
  - answerable 2 stayed `declared`
  - PDF jump/preview worked during the runs
  - refusal stayed `retrieval_gate / retrieval_no_match`
- Run timing window:
  - run 1: `56s`
  - run 2: `67s`
  - run 3: `24s`
- Honest caveat:
  - this operator rehearsal reused the already-loaded locked sample document after warmup
  - it is therefore a warm demo reproducibility pass rather than a stricter cold-start upload-from-zero pass
- Practical meaning:
  - for the current competition/demo goal, `G3` is no longer the active blocker
  - the next work should shift to final submission-material polish and final export freeze

## Real In-Project Minimal Path Validation (`2026-04-18`)

- Environment note:
  - current active `.env` is the new `Wuwen Xinqiong` config
  - old replay reports using prior providers should be treated as historical only
- Validation sample:
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
- Answerable path:
  - `login -> upload -> ask -> citation -> PDF page -> PDF render`: passed
  - returned model: `qwen3-235b-a22b-instruct-2507`
  - `ask` latency: about `6686 ms`
  - retrieval status: `matched`
  - citation count: `2`
  - cited page fetch: passed
  - cited page render (`image/png`): passed
- True off-topic refusal check:
  - question: `木星有几颗卫星？`
  - result: refused correctly
  - retrieval status: `no_match`
  - latency: about `38 ms`
- Caution:
  - a semi-related "refusal" prompt that still mentions document entities (for example `作者`) may retrieve matching chunks and produce an answer
  - the final refusal demo prompt should therefore be purely off-topic
- Debugging note:
  - one earlier local false negative came from PowerShell -> inline Python encoding turning Chinese prompt literals into `?`
  - that was a validation harness issue, not a project retrieval bug

## Gold Sample Candidate Lock (`2026-04-18`)

- Candidate PDF:
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
- Candidate prompt set:
  - answerable 1: `这篇论文主要研究了什么问题？`
  - answerable 2: `作者最终的方法排名和总体准确率分别是多少？`
  - refusal: `木星有几颗卫星？`
- Candidate manifest saved at:
  - `evidence/materials/GOLD_SAMPLE_CANDIDATE_20260418.json`

## QA Model Comparison (`2026-04-18`)

- Reusable comparison script added:
  - `scripts/compare_qa_models.py`
- Latest report outputs:
  - `evidence/reports/gold_sample_qa_compare_latest.md`
  - `evidence/reports/gold_sample_qa_compare_latest.json`
- Compared models:
  - `qwen3-235b-a22b-instruct-2507`
  - `qwen3-32b`
- Result:
  - both models passed `2 answerable + 1 refusal`
  - both answerable prompts returned citations and passed page/render validation
  - both models refused the off-topic prompt correctly
- Latency summary:
  - `qwen3-235b-a22b-instruct-2507`: average about `4896 ms`
  - `qwen3-32b`: average about `4396 ms`
- Quality/citation observation:
  - `qwen3-235b-a22b-instruct-2507` returned slightly richer grounding on the broader research-focus question
  - `qwen3-32b` was slightly faster, but typically returned fewer citations/evidence quotes
- Current decision:
  - keep `qwen3-235b-a22b-instruct-2507` as the primary `MODEL_QA`
  - keep `qwen3-32b` as the validated fallback option

## Replay Workflow Refresh (`2026-04-18`)

- `scripts/replay_sample_set.py` has been updated to match the current runtime boundary:
  - creates a controlled-alpha session internally
  - uploads documents under the current session owner
  - passes `session_id` + `document_access_token` into task execution
  - can now read both:
    - the old broad sample-set manifest format
    - the new gold-sample candidate manifest format
- `scripts/run_real_replay.ps1` now accepts:
  - `-Manifest`
  - `-NamePrefix`
- Real gold-sample replay refreshed successfully:
  - latest report: `evidence/reports/gold_sample_replay_real_latest.md`
  - latest summary: `evidence/reports/gold_sample_replay_real_summary_latest.md`
- Real gold-sample replay result under current primary `MODEL_QA`:
  - `2 answered + 1 refused`
  - `0 errors`
  - answerable citations present
  - refusal remained `retrieval_no_match`

## Doc / Material Alignment (`2026-04-18`)

- Runtime/deploy docs now align to the current Wuwen Xinqiong baseline:
  - `.env.example`
  - `README.md`
  - `WORKLOG.md`
  - `render.yaml`
  - `docs/DEPLOY_RENDER.md`
- Competition-facing materials now treat the locked gold-sample path as primary:
  - `evidence/materials/SAMPLE_SET.md`
  - `evidence/materials/PROJECT_ONE_PAGER.md`
  - `evidence/materials/REAL_REPLAY_GUIDE.md`
  - `evidence/materials/MATERIALS_INDEX.md`
- Broader sample-set replay is still available, but should now be treated as secondary coverage rather than the default judging/demo evidence path

## Screenshot Refresh (`2026-04-18`)

- Automated screenshot script added:
  - `scripts/capture_gold_sample_screenshots.js`
- The script uses:
  - current local `.env`
  - real session/login boundary
  - locked gold-sample PDF upload
  - the locked `2 answerable + 1 refusal` prompt path
- Refreshed screenshot outputs:
  - `evidence/screenshots/20260418_gold_ask_research_focus.png`
  - `evidence/screenshots/20260418_gold_pdf_render.png`
  - `evidence/screenshots/20260418_gold_ask_rank_accuracy.png`
  - `evidence/screenshots/20260418_gold_refusal.png`
  - `evidence/screenshots/20260418_stats_panel.png`
  - `evidence/screenshots/20260418_api_docs.png`
- Practical meaning:
  - the screenshot-evidence gap for the locked judging/demo pack is now closed

## Competition Asset Pack (`2026-04-18`)

- New asset-pack doc added:
  - `evidence/materials/COMPETITION_ASSET_PACK.md`
- Purpose:
  - map the locked gold-sample screenshots, reports, and fixed wording into a single source for:
    - PPT
    - demo video
    - poster
    - spoken defense wording
- Related materials now aligned around the same gold-sample-primary story:
  - `evidence/materials/SUBMISSION_PREP_GUIDE.md`
  - `evidence/materials/MATERIALS_INDEX.md`

## Submission Deliverables (`2026-04-18`)

- Ready-to-use drafting docs added:
  - `evidence/materials/PPT_DECK_6SLIDES.md`
  - `evidence/materials/VIDEO_SHOTLIST_2MIN.md`
  - `evidence/materials/POSTER_COPY.md`
- Export helper added:
  - `scripts/export_competition_asset_pack.ps1`
- Printable HTML prototypes added:
  - `deliverables/competition_kit/deck.html`
  - `deliverables/competition_kit/poster.html`
- PDF export helper added:
  - `scripts/export_competition_pdfs.js`
- Current exported PDFs:
  - `deliverables/competition_kit/deck.pdf`
  - `deliverables/competition_kit/poster.pdf`
- Updated asset-bundle export:
  - `scripts/export_competition_asset_pack.ps1` now includes the current HTML/PDF deliverables and `scripts/export_competition_pdfs.js`
- Video subtitle baseline added:
  - `deliverables/competition_kit/video_subtitles.srt`
- Practical meaning:
  - the repo no longer stops at “asset collection”
  - the next operator can draft PPT / video / poster directly from repo-native materials
  - there is now also a near-final visual baseline for deck/poster production
  - deck/poster PDF export can now be reproduced from the repo rather than by manual browser steps
  - a timestamped bundle can be exported for handoff without manually re-picking files

## Current Meaning

- Wuwen Xinqiong integration itself is no longer the blocker
- The project has moved from “external API validation” to “real in-project flow validation”
- The main demo chain `ask -> citation -> PDF` has now been verified in-project under the current Wuwen Xinqiong `.env`
- A Chinese gold-sample candidate and candidate question set are now locked for the current stage
- The current `MODEL_QA` decision can remain on `qwen3-235b-a22b-instruct-2507` without blocking `G2`
- The replay/evidence tooling is now aligned with the current session/access-token runtime posture
- The repo docs/materials are now aligned around that locked gold-sample path instead of the older broader replay path
- The locked gold-sample screenshot set is now refreshed under the current real runtime
- The repo now has a single asset-pack document for assembling final competition materials without re-deciding facts
- The repo now also contains first-pass PPT / video / poster drafting docs plus a one-click export path for handoff packaging
- The repo now contains printable HTML deck/poster prototypes, so the next operator can move straight into final PDF / slide production
- The repo now has a direct script path for exporting deck/poster PDFs from those HTML prototypes
- The repo now already contains one generated deck PDF and one generated poster PDF as the current baseline outputs
- The handoff/export bundle can now carry those HTML/PDF deliverables forward without manual file picking
- The repo now also contains a timed subtitle baseline for the 2-minute demo video
- The previous fresh-Q2 `candidate` instability has now been fixed and independently rechecked with `3 / 3` fresh declared runs
- `G1`: pass
- `G2`: pass
- `G3`: pass (warm operator rehearsal)

## Review-Driven Hardening (`2026-04-19`)

- External-review findings were translated into code/material fixes:
  - `frontend/src/App.tsx` now prefers the validated quote in `declared` mode for both automatic preview state and citation-click preview state
  - `frontend/src/components/ResultPanel.tsx` now exposes `evidence-mode-*` test ids and treats retrieval-gated refusals as `执行路径: retrieval_gate（未调用模型）`, hiding request ID on that path
  - `backend/app/services/model_client.py` now explicitly requires at least one verbatim evidence quote for `ask`
  - `backend/app/services/task_service.py` now:
    - labels retrieval-gated refusals as `model_name="retrieval_gate"`
    - strips punctuation drift during quote normalization
    - stops silently coercing plain-string quotes onto the first chunk
  - `scripts/capture_gold_sample_screenshots.js` now:
    - retries answerable screenshots until `evidence_mode=declared`
    - cache-busts retries with zero-width prompt variants
    - writes `.json` sidecars beside ask/refusal screenshots
  - competition materials now keep `stats_panel` / `api_docs` appendix-only in the main story docs
- Verification completed:
  - `npm run build`
  - `npm test -- --run` -> `7 passed`
  - `.venv\Scripts\python.exe -m pytest` -> `55 passed`
  - `node scripts\capture_gold_sample_screenshots.js` refreshed:
    - `evidence/screenshots/20260419_gold_ask_research_focus.png`
    - `evidence/screenshots/20260419_gold_pdf_render.png`
    - `evidence/screenshots/20260419_gold_ask_rank_accuracy.png`
    - `evidence/screenshots/20260419_gold_refusal.png`
    - `evidence/screenshots/20260419_stats_panel.png`
    - `evidence/screenshots/20260419_api_docs.png`
  - sidecar metadata confirms:
    - `20260419_gold_ask_research_focus.json` -> `evidence_mode=declared`
    - `20260419_gold_ask_rank_accuracy.json` -> `evidence_mode=declared` on attempt `2`
    - `20260419_gold_refusal.json` -> `evidence_mode=none`
  - `node scripts\export_competition_pdfs.js` refreshed:
    - `deliverables/competition_kit/deck.pdf`
    - `deliverables/competition_kit/poster.pdf`
  - `scripts/export_competition_asset_pack.ps1` now auto-detects the latest screenshot date prefix and exports sidecar metadata; latest pack:
    - `evidence/exports/competition_asset_pack_20260419_144125/`
- Practical meaning:
  - the previously identified judge-facing mismatch (`candidate` screenshot mixed into the locked answerable path) is now closed in the current repo state
  - the PDF preview snippet/highlight mismatch is now closed for `declared` ask results in the frontend
  - the export/handoff path now follows the latest screenshot refresh without manual date-string edits

## Material Freeze Rebuild (`2026-04-19`)

- Trigger:
  - targeted external review correctly flagged that the competition-material chain was not freeze-ready:
    - corrupted Chinese drafting docs
    - broken HTML deliverables
    - `deck.pdf` / `poster.pdf` page counts not matching the intended judged-demo outputs
- Clean-source rebuild completed:
  - rebuilt source docs:
    - `evidence/materials/PPT_DECK_6SLIDES.md`
    - `evidence/materials/VIDEO_SHOTLIST_2MIN.md`
    - `evidence/materials/POSTER_COPY.md`
    - `evidence/materials/COMPETITION_ASSET_PACK.md`
  - rebuilt deliverable sources:
    - `deliverables/competition_kit/deck.html`
    - `deliverables/competition_kit/poster.html`
  - hardened export path:
    - `scripts/export_competition_pdfs.js`
      - now rejects malformed HTML patterns
      - now rejects known mojibake markers
      - now rejects incorrect PDF page counts
- Verification after rebuild:
  - `node scripts\export_competition_pdfs.js`
  - confirmed outputs:
    - `deliverables/competition_kit/deck.pdf` -> `6` pages
    - `deliverables/competition_kit/poster.pdf` -> `1` page
  - UTF-8 reads of the rebuilt HTML files show:
    - `研答通`
    - `upload → ask → citation → PDF → refusal`
    - no known mojibake markers
- Practical meaning:
  - the current blocker has shifted away from “broken submission materials”
  - the repo again has a sane printable baseline for deck/poster work
  - future exports now fail fast instead of silently producing a bad `deck/poster` PDF baseline

## Freeze Fact Reference

- Prefer this file when another operator or another AI needs the current authoritative judged-demo facts:
  - `agent_handoff/FREEZE_FACT_SHEET_20260419.md`

## Recommended Next Step

1. Export a refreshed competition handoff bundle so the rebuilt `deck/poster` outputs replace the previously broken printable baseline
2. Use `agent_handoff/FREEZE_FACT_SHEET_20260419.md` as the first file for any further external review or operator handoff
3. If another judging-risk review is needed, regenerate the review bundle from the rebuilt material state first
4. If deployment/demo latency becomes a practical issue, rerun the same compare script before switching `MODEL_QA` to `qwen3-32b`
5. Keep the broader sample-set replay as secondary coverage only unless wider capability sampling is explicitly needed
6. Do not expand product scope while final materials are being assembled
