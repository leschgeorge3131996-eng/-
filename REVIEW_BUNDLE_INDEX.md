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

The project is in a late-stage competition sprint. The team has already narrowed
the story on purpose:

- strongest feature: evidence-backed `ask`
- main live chain: `upload -> ask -> citation -> PDF -> refusal`
- judging priority: trust and reproducibility over feature breadth

This bundle should be reviewed as a near-freeze competition project, not as a
generic SaaS startup.

## Current Snapshot

- Runtime provider:
  - `Wuwen Xinqiong`
- Primary QA model:
  - `qwen3-235b-a22b-instruct-2507`
- Validated fallback:
  - `qwen3-32b`
- Locked sample:
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
- Current strongest evidence:
  - strict `G3` fresh-upload three-run pass at
    `evidence/experiments/20260420_g3_strict_rehearsal.md`
- Current judged-asset source drafts:
  - `evidence/materials/PPT_DECK_3PAGES_FINAL.md`
  - `evidence/materials/VIDEO_SHOTLIST_5MIN_FINAL.md`
- Current repo-native production baselines:
  - `deliverables/competition_kit/deck_3page_final.pdf`
  - `deliverables/competition_kit/video_subtitles_5min_final.srt`

## What Is Already Done

- real provider path validated
- locked sample and prompt triad fixed
- fresh Q2 evidence regression fixed and rechecked
- strict `G3` recorded with request-id traceability
- judge-facing proof pages assembled
- repo-native `3`-page deck PDF baseline exported
- repo-native `5`-minute subtitle baseline written
- export bundles for handoff and review can now be regenerated from scripts

## What Is Still Open

Only last-mile asset production remains by default:

- final native `PPT`
- final edited `5`-minute video
- screenshot refresh only if target environment changes

## What The Reviewer Should Pay Attention To

1. Whole-project credibility, not just one document.
2. Whether the current evidence-backed story is strong enough for judging.
3. Whether current docs, deliverables, and code claims are internally consistent.
4. Whether any hidden implementation or presentation risk could still hurt the
   team live.
5. Whether the team is wasting time on the wrong last-mile tasks.

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
3. `agent_handoff/FREEZE_FACT_SHEET_20260419.md`
4. `agent_handoff/TASK_BOARD.md`
5. `agent_handoff/PROJECT_HANDOFF.md`
6. `evidence/materials/COMPETITION_ASSET_PACK.md`
7. `evidence/materials/SUBMISSION_SPEC_CROSSWALK.md`
8. `evidence/experiments/20260420_g3_strict_rehearsal.md`
9. current deliverables under `deliverables/competition_kit/`
10. code paths only where needed to verify a claim

## Bundle Notes

When `scripts/export_review_bundle.ps1` generates a fresh review bundle, the
stage directory will also contain a generated `BUNDLE_MANIFEST.md` that lists
the exact copied files and generation metadata for that specific bundle.
