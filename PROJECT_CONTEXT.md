# Project Context

## Background

YanDatong is a competition-focused document QA project for paper reading,
report review, and defense preparation. Its core differentiator is not generic
"chat over files", but an evidence-backed `ask` flow that can:

- answer from retrieved document evidence
- return citation blocks and evidence snippets
- jump back into the cited PDF page
- refuse unsupported off-topic questions instead of fabricating

The team is in a late-stage competition sprint. This is not a broad product
discovery phase and not a public SaaS expansion phase.

## Goal Of This External Review

Review the whole project end-to-end as it exists today:

- product positioning
- code / architecture
- demo path credibility
- evidence chain (including the newly landed extended evaluation)
- submission materials
- remaining risks before final freeze

The purpose is to decide whether the current project state is strong enough for
external judging and what minimum remaining work is still required.

## Current Snapshot (as of 2026-04-21)

- Project name: `YanDatong`
- Current positioning:
  - evidence-backed document QA for paper/report reading and defense prep
- Runtime provider:
  - `Wuwen Xinqiong`
- Primary QA model:
  - `qwen3-235b-a22b-instruct-2507`
- Validated fallback:
  - `qwen3-32b`
- Locked gold-sample document:
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
- Locked demo path:
  - `upload -> ask -> citation -> PDF -> refusal`
- Extended eval corpus (4 documents):
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
  - `evidence/samples/attention_is_all_you_need.pdf`
  - `evidence/samples/paper_report.md`
  - `evidence/samples/research_brief.md`

## What Is Already Closed

### Real-path end-to-end

- Real provider path (Wuwen Xinqiong) is live and validated in-project.
- Gold-sample replay reports and screenshot evidence exist.
- Q2 fresh declared-evidence instability was fixed and rechecked.
- Strict `G3` is now recorded as a fresh-upload three-run pass with request-id
  traceability:
  - `evidence/experiments/20260420_g3_strict_rehearsal.md`

### Quantitative evaluation (new on 2026-04-21)

Two layers of numbers now exist side by side:

- Strict G3 / locked gold path (`3` prompts × `3` runs, `9` entries):
  - evidence declaration rate: `100%`
  - citation page accuracy: `100%`
  - retrieval page coverage: `100%`
  - evidence quote rate: `100%`
  - refusal precision: `100%`
  - cross-run consistency: `100%`
  - chunk utilization: `38%`
  - avg answerable latency: `5521 ms`
  - script: `scripts/compute_eval_metrics.py`
  - report: `evidence/reports/quantitative_eval_metrics.md`
- Extended eval v1 (`51` cases across the 4 documents above):
  - overall pass: `46 / 51` (`90.2%`)
  - refusal precision: `100%`
  - citation accuracy: `88.4%`
  - declaration rate: `88.4%`
  - avg latency: `~5.2 s`
  - manifest: `evidence/materials/EXTENDED_EVAL_V1.json`
  - refusal-only slice: `evidence/materials/EXTENDED_EVAL_V1_REFUSAL_ONLY.json`
  - scope note: `evidence/materials/EXTENDED_EVAL_SCOPE.md`
  - latest report: `evidence/reports/extended_eval_v1_latest.md`

### Late-stage engineering hardening (2026-04-21)

- LLM-layer refusal escape: `ask` prompt now returns structured `refused=true`
  on out-of-scope, and `TaskService` routes that into a dedicated
  `llm_refused` branch. This fixed a root cause where the retry loop used to
  pressure the model into fabrication. Refusal precision on the 20-seed
  extended eval went `0%` → `100%`.
- Retrieval metadata-intent fallback: author/affiliation/contribution queries
  now pin `chunked_document.chunks[0]` so first-page metadata is not missed
  by top-k. This lifted overall extended-eval pass `85%` → `95%` on the
  20-seed and held on the 51-case expansion.
- `scripts/predeploy_sanity.py` now exists as a one-command pre-demo
  must-pass: archive `call_logs.jsonl`, run the 3 gold cases via real
  `TaskService`, emit a markdown report, exit 0 only on `3/3`. Wired as the
  first step in `DEFENSE_DEMO_RISK_CHECKLIST.md` and the fast-path in
  `GOLD_SAMPLE_RUNBOOK.md`.

### Frontend UX polish (2026-04-21)

- evidence confidence bar: three-dot signal
  (green=declared / orange=candidate / red=none) with citation + quote counts
- citation cards are now fully clickable buttons that jump to PDF preview
- dedicated refusal card replaces the old plain warning text
- drag-and-drop upload zone with hover feedback
- hero button pulse animation
- all `7` frontend smoke tests still pass and `npm run build` is clean

### Judge-facing proof pages

- `evidence/materials/PRODUCT_TECHNICAL_WRITEUP.md`
- `evidence/materials/PLATFORM_USAGE_EVIDENCE.md`
- `evidence/materials/HARD_EVIDENCE_SUMMARY.md` (updated §7 with dual
  strict-G3 + 51-case numbers)
- `evidence/materials/SCORING_EVIDENCE_MATRIX.md` (updated 量化指标 row)

### Judged submission assets

- Official submission source drafts already exist:
  - `evidence/materials/PPT_DECK_3PAGES_FINAL.md`
  - `evidence/materials/VIDEO_SHOTLIST_5MIN_FINAL.md`
- Repo-native final production baselines already exist:
  - `deliverables/competition_kit/deck_3page_final.html`
  - `deliverables/competition_kit/deck_3page_final.pdf`
  - `deliverables/competition_kit/video_subtitles_5min_final.srt`

## What Is Still Open

Only last-mile non-engineering work remains by default:

- final native `PPT` (teammate production, source draft already exists)
- final recorded / edited `5`-minute demo video (teammate production,
  shotlist and subtitles already exist)
- full dry-run rehearsal on the actual judging environment (including
  `DEMO_MODE=true` verification and `predeploy_sanity.py` as first step)
- one final screenshot refresh only if the target judging environment changes

There is currently no hard engineering blocker open by default.

## Important Review Constraint

This review should judge the current project honestly, but it should not drift
into broad-scope product brainstorming.

Do not optimize for:

- new task types
- OCR-heavy redesigns
- local-model branches
- public SaaS reframing
- large frontend redesigns
- long-term product pivots unrelated to the current competition goal

## How To Resolve Contradictions

If older historical notes conflict with newer files, prefer in this order:

1. `agent_handoff/SESSION_LOG.md` (latest entries first — 2026-04-21 block)
2. `agent_handoff/TASK_BOARD.md`
3. `agent_handoff/PROJECT_HANDOFF.md`
4. `agent_handoff/FREEZE_FACT_SHEET_20260419.md`
5. `evidence/experiments/20260420_g3_strict_rehearsal.md`
6. `evidence/reports/quantitative_eval_metrics.md`
7. `evidence/reports/extended_eval_v1_latest.md`
8. current deliverables under `deliverables/competition_kit/`

Treat stale historical notes as context, not as the final truth layer.

## What The Reviewer Should Decide

1. Is the whole project story clear, credible, and competition-ready?
2. Is the evidence-backed `ask` path strong enough to carry judging?
3. Is the 51-case extended eval (`46 / 51` pass, with `5` honestly disclosed
   failures) a net positive for credibility, or does it open a judging risk?
4. Are the current code and architecture solid enough for the claimed demo?
5. Are the current materials internally consistent?
6. What are the few remaining high-leverage risks before final submission?

## Recommended Reading Order

1. `PROJECT_CONTEXT.md` (this file)
2. `REVIEW_PROMPT.md`
3. `REVIEW_BUNDLE_INDEX.md`
4. `agent_handoff/SESSION_LOG.md` (latest 2026-04-21 entries first)
5. `agent_handoff/TASK_BOARD.md`
6. `agent_handoff/PROJECT_HANDOFF.md`
7. `agent_handoff/FREEZE_FACT_SHEET_20260419.md`
8. `evidence/materials/HARD_EVIDENCE_SUMMARY.md` (§7 dual-metric block)
9. `evidence/materials/SCORING_EVIDENCE_MATRIX.md`
10. `evidence/reports/quantitative_eval_metrics.md`
11. `evidence/reports/extended_eval_v1_latest.md`
12. `evidence/experiments/20260420_g3_strict_rehearsal.md`
13. `evidence/materials/PPT_DECK_3PAGES_FINAL.md`
14. `evidence/materials/VIDEO_SHOTLIST_5MIN_FINAL.md`
15. current deliverables under `deliverables/competition_kit/`
16. backend code paths only where needed to verify a claim (start at
    `backend/app/services/task_service.py` and
    `backend/app/services/retrieval_service.py`)
