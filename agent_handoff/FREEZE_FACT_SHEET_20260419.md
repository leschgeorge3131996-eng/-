# Freeze Fact Sheet (`2026-04-19`)

Use this file as the quickest authoritative reference when another operator or another AI needs the current judged-demo status without re-reading all historical notes.

## Main Story

- Keep the judged-demo story fixed to:
  - `upload -> ask -> citation -> PDF -> refusal`
- Do **not** present `login` / invite flow as a product capability
- Do **not** expand scope back into generic chat / SaaS framing

## Locked Demo Inputs

- Locked sample:
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
- Locked prompt triad:
  - `这篇论文主要研究了什么问题？`
  - `作者最终的方法排名和总体准确率分别是多少？`
  - `木星有几颗卫星？`

## Runtime Facts

- Current active provider path:
  - `Wuwen Xinqiong`
- Current default `MODEL_QA`:
  - `qwen3-235b-a22b-instruct-2507`
- Validated fallback:
  - `qwen3-32b`

## Verification Facts

- Frontend tests:
  - `npm test -- --run` -> `7 passed`
- Frontend build:
  - `npm run build` -> passed
- Backend tests:
  - `.venv\Scripts\python.exe -m pytest` -> `55 passed`
- Q2 fresh evidence check:
  - `evidence/experiments/20260419_q2_declared_stability_check.md`
  - result: `3 / 3` fresh local runs returned `declared`

## Gate Wording

- `G1`: pass
- `G2`: pass
- `G3`: pass for the current **warm-state operator rehearsal** path
- Honest caveat for `G3`:
  - current recorded rehearsal is **not** the stricter upload-from-zero cold-start + second-operator version
  - if a stricter judging requirement appears, treat that as an additional rehearsal task rather than reopening the engineering chain

## Material Freeze Facts

- Clean source drafting docs were rebuilt on `2026-04-19`:
  - `evidence/materials/PPT_DECK_6SLIDES.md`
  - `evidence/materials/VIDEO_SHOTLIST_2MIN.md`
  - `evidence/materials/POSTER_COPY.md`
  - `evidence/materials/COMPETITION_ASSET_PACK.md`
- Printable deliverables were rebuilt and re-exported:
  - `deliverables/competition_kit/deck.html`
  - `deliverables/competition_kit/poster.html`
  - `deliverables/competition_kit/deck.pdf` -> `6` pages
  - `deliverables/competition_kit/poster.pdf` -> `1` page
- PDF export now has sanity checks in:
  - `scripts/export_competition_pdfs.js`

## Latest Judge-Facing Evidence Set

- Screenshots:
  - `evidence/screenshots/20260419_gold_ask_research_focus.png`
  - `evidence/screenshots/20260419_gold_pdf_render.png`
  - `evidence/screenshots/20260419_gold_ask_rank_accuracy.png`
  - `evidence/screenshots/20260419_gold_refusal.png`
- Current rehearse/export bundle before the next refresh:
  - `evidence/exports/competition_asset_pack_20260419_165205/`

## What Still Matters

1. Keep materials, screenshots, and handoff docs aligned to this fact sheet.
2. If another export bundle is created, ensure it carries the rebuilt `deck/poster` outputs.
3. If another AI reviews the project, point it here first so it does not over-index on stale `54 passed`, older screenshot prefixes, or pre-rebuild material corruption.
