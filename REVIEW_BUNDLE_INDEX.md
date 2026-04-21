# Review Bundle Index

## Purpose

This review bundle is for an external AI to judge the current whole-project
state of `YanDatong`.

The aim is not broad ideation. The aim is to answer:

- how strong the project currently is
- whether the evidence chain is credible
- whether the demo / materials / code are aligned
- what minimum work still remains before confident final submission

## Background

The project is in a late-stage competition sprint. The team has already
narrowed the story on purpose:

- strongest feature: evidence-backed `ask`
- main live chain: `upload -> ask -> citation -> PDF -> refusal`
- judging priority: trust and reproducibility over feature breadth

This bundle should be reviewed as a near-freeze competition project, not as a
generic SaaS startup.

## Current Snapshot (2026-04-21)

- Runtime provider:
  - `Wuwen Xinqiong`
- Primary QA model:
  - `qwen3-235b-a22b-instruct-2507`
- Validated fallback:
  - `qwen3-32b`
- Locked gold-sample document:
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
- Extended eval corpus (4 documents):
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
  - `evidence/samples/attention_is_all_you_need.pdf`
  - `evidence/samples/paper_report.md`
  - `evidence/samples/research_brief.md`
- Current strongest evidence:
  - strict `G3` fresh-upload three-run pass at
    `evidence/experiments/20260420_g3_strict_rehearsal.md`
  - strict G3 quantitative metrics at
    `evidence/reports/quantitative_eval_metrics.md`
  - extended 51-case eval report at
    `evidence/reports/extended_eval_v1_latest.md`
- Current judged-asset source drafts:
  - `evidence/materials/PPT_DECK_3PAGES_FINAL.md`
  - `evidence/materials/VIDEO_SHOTLIST_5MIN_FINAL.md`
- Current repo-native production baselines:
  - `deliverables/competition_kit/deck_3page_final.pdf`
  - `deliverables/competition_kit/video_subtitles_5min_final.srt`

## What Is Already Done

### End-to-end / demo path

- real provider path validated
- locked sample and prompt triad fixed
- fresh Q2 evidence regression fixed and rechecked
- strict `G3` recorded with request-id traceability

### Quantitative evaluation (2026-04-21)

- strict G3 metrics computed: 4 rates at `100%`, refusal precision `100%`,
  cross-run consistency `100%`, chunk utilization `38%`, avg latency
  `5521 ms`
- extended v1 (`51` cases × 4 docs): `46 / 51` pass (`90.2%`), refusal
  precision `100%`, citation accuracy `88.4%`
- `5` remaining failures kept honestly, not prompt-tuned away
- `scripts/predeploy_sanity.py` wired as pre-demo must-pass

### Late-stage hardening (2026-04-21)

- LLM-layer refusal escape (`refused=true` JSON contract + dedicated
  `llm_refused` branch in `TaskService`) — refusal precision on extended
  seed `0%` → `100%`
- metadata-intent retrieval fallback (first-chunk pin on
  author/affiliation/contribution queries) — overall pass `85%` → `95%`
- frontend UX polish (three-dot confidence bar, clickable citations,
  dedicated refusal card, drag-and-drop upload, hero pulse); `7 / 7` smoke
  tests pass; build clean

### Judge-facing materials

- judge-facing proof pages assembled and updated:
  - `evidence/materials/HARD_EVIDENCE_SUMMARY.md` (§7 dual-metric block)
  - `evidence/materials/SCORING_EVIDENCE_MATRIX.md` (量化指标 row)
- repo-native `3`-page deck PDF baseline exported
- repo-native `5`-minute subtitle baseline written
- export bundles for handoff and review can now be regenerated from scripts

## What Is Still Open

Only last-mile non-engineering work remains by default:

- final native `PPT` (teammate production)
- final edited `5`-minute video (teammate production)
- full rehearsal on the target judging environment
  (`DEMO_MODE=true` + `predeploy_sanity.py` as the first step)
- screenshot refresh only if target environment changes

## What The Reviewer Should Pay Attention To

1. Whole-project credibility, not just one document.
2. Whether the current evidence-backed story is strong enough for judging.
3. Whether the dual-layer evaluation (strict-G3 100% + extended 90.2%)
   strengthens the story or introduces a judging risk that the team should
   prepare for.
4. Whether current docs, deliverables, and code claims are internally
   consistent.
5. Whether any hidden implementation or presentation risk could still hurt
   the team live.
6. Whether the team is wasting time on the wrong last-mile tasks.

## What Not To Over-focus On

- new task types
- OCR-heavy redesigns
- local-model branches
- public SaaS expansion
- broad product pivots
- large cosmetic rewrites

## Read In This Order

1. `PROJECT_CONTEXT.md`
2. `REVIEW_PROMPT.md`
3. `agent_handoff/SESSION_LOG.md` (top block = 2026-04-21, the most
   current truth)
4. `agent_handoff/TASK_BOARD.md`
5. `agent_handoff/PROJECT_HANDOFF.md`
6. `agent_handoff/FREEZE_FACT_SHEET_20260419.md`
7. `evidence/materials/HARD_EVIDENCE_SUMMARY.md`
8. `evidence/materials/SCORING_EVIDENCE_MATRIX.md`
9. `evidence/reports/quantitative_eval_metrics.md`
10. `evidence/reports/extended_eval_v1_latest.md`
11. `evidence/experiments/20260420_g3_strict_rehearsal.md`
12. `evidence/materials/PPT_DECK_3PAGES_FINAL.md`
13. `evidence/materials/VIDEO_SHOTLIST_5MIN_FINAL.md`
14. current deliverables under `deliverables/competition_kit/`
15. backend code only when a claim needs to be verified — start at
    `backend/app/services/task_service.py` and
    `backend/app/services/retrieval_service.py`

## Bundle Notes

When `scripts/export_review_bundle.ps1` generates a fresh review bundle, the
stage directory will also contain a generated `BUNDLE_MANIFEST.md` that lists
the exact copied files and generation metadata for that specific bundle.
