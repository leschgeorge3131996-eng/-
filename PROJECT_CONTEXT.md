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
- evidence chain
- submission materials
- remaining risks before final freeze

The purpose is to decide whether the current project state is strong enough for
external judging and what minimum remaining work is still required.

## Current Snapshot

- Project name: `YanDatong`
- Current positioning:
  - evidence-backed document QA for paper/report reading and defense prep
- Runtime provider:
  - `Wuwen Xinqiong`
- Primary QA model:
  - `qwen3-235b-a22b-instruct-2507`
- Validated fallback:
  - `qwen3-32b`
- Locked sample:
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
- Locked demo path:
  - `upload -> ask -> citation -> PDF -> refusal`

## What Is Already Closed

- Real provider path is live and validated in-project.
- Gold-sample replay reports and screenshot evidence exist.
- Q2 fresh declared-evidence instability was fixed and rechecked.
- Strict `G3` is now recorded as a fresh-upload three-run pass with request-id
  traceability:
  - `evidence/experiments/20260420_g3_strict_rehearsal.md`
- Judge-facing proof pages are already assembled:
  - `PRODUCT_TECHNICAL_WRITEUP.md`
  - `PLATFORM_USAGE_EVIDENCE.md`
  - `HARD_EVIDENCE_SUMMARY.md`
  - `SCORING_EVIDENCE_MATRIX.md`
- Official submission source drafts already exist:
  - `PPT_DECK_3PAGES_FINAL.md`
  - `VIDEO_SHOTLIST_5MIN_FINAL.md`
- Repo-native final production baselines already exist:
  - `deliverables/competition_kit/deck_3page_final.html`
  - `deliverables/competition_kit/deck_3page_final.pdf`
  - `deliverables/competition_kit/video_subtitles_5min_final.srt`

## What Is Still Open

Only last-mile asset production remains:

- final native `PPT`
- final recorded / edited `5`-minute demo video
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

If older historical notes conflict with newer files, prefer:

1. `agent_handoff/FREEZE_FACT_SHEET_20260419.md`
2. `agent_handoff/TASK_BOARD.md`
3. `agent_handoff/PROJECT_HANDOFF.md`
4. `evidence/experiments/20260420_g3_strict_rehearsal.md`
5. current deliverables under `deliverables/competition_kit/`

Treat stale historical notes as context, not as the final truth layer.

## What The Reviewer Should Decide

1. Is the whole project story clear, credible, and competition-ready?
2. Is the evidence-backed `ask` path strong enough to carry judging?
3. Are the current code and architecture solid enough for the claimed demo?
4. Are the current materials internally consistent?
5. What are the few remaining high-leverage risks before final submission?

## Recommended Reading Order

1. `PROJECT_CONTEXT.md`
2. `REVIEW_PROMPT.md`
3. `REVIEW_BUNDLE_INDEX.md`
4. `agent_handoff/FREEZE_FACT_SHEET_20260419.md`
5. `agent_handoff/TASK_BOARD.md`
6. `agent_handoff/PROJECT_HANDOFF.md`
7. `evidence/materials/COMPETITION_ASSET_PACK.md`
8. `evidence/materials/SUBMISSION_SPEC_CROSSWALK.md`
9. `evidence/experiments/20260420_g3_strict_rehearsal.md`
10. current deliverables under `deliverables/competition_kit/`
11. code paths only where needed to verify a claim
