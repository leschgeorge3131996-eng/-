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
  - `54 passed`

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

## Recommended Next Step

1. Run `powershell -ExecutionPolicy Bypass -File .\scripts\export_competition_asset_pack.ps1` and use the exported full bundle as the source for any last-mile polish or external handoff
2. If deployment/demo latency becomes a practical issue, rerun the same compare script before switching `MODEL_QA` to `qwen3-32b`
3. Keep the broader sample-set replay as secondary coverage only unless wider capability sampling is explicitly needed
4. Do not expand product scope while final materials are being assembled
