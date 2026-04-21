# External Review Prompt

Before writing your judgment, read these files first (in this order):

1. `PROJECT_CONTEXT.md`
2. `REVIEW_BUNDLE_INDEX.md`
3. `agent_handoff/SESSION_LOG.md` — the top block (2026-04-21) is the most
   current truth
4. `agent_handoff/TASK_BOARD.md`
5. `agent_handoff/PROJECT_HANDOFF.md`
6. `evidence/reports/quantitative_eval_metrics.md`
7. `evidence/reports/extended_eval_v1_latest.md`
8. `agent_handoff/FREEZE_FACT_SHEET_20260419.md`

## Background

This is a late-stage review for `YanDatong`, a competition-focused document QA
project. The team is not asking for broad product ideation. They are asking for
a hard external review of the whole project as it exists now.

The current strategy is intentionally narrow:

- center the story on evidence-backed `ask`
- prove `ask -> citation -> PDF back-link -> refusal`
- maximize judging credibility
- avoid reopening scope unless a real blocker is found

## Goal

Judge whether the project, taken as a whole, is genuinely close to final
submission / judging freeze.

You should evaluate:

- product positioning
- architecture / code credibility
- demo path credibility
- evidence and material consistency (including the newly landed 51-case
  extended evaluation)
- remaining high-leverage risks

Do not turn this into a generic SaaS roadmap review.

## Important Current Facts (as of 2026-04-21)

### Runtime

- Runtime provider is already switched to `Wuwen Xinqiong`.
- Primary QA model: `qwen3-235b-a22b-instruct-2507`
- Validated fallback: `qwen3-32b`
- Locked gold-sample document and prompt triad already exist.
- Strict `G3` is recorded as a fresh-upload three-run pass:
  - `evidence/experiments/20260420_g3_strict_rehearsal.md`

### Two layers of quantitative evidence now coexist

- **Strict G3 / locked gold path** (`3` prompts × `3` runs = `9` entries):
  - 4 rates at `100%` (evidence declaration, citation page accuracy,
    retrieval page coverage, evidence quote rate)
  - refusal precision `100%`, cross-run consistency `100%`
  - chunk utilization `38%`, avg answerable latency `5521 ms`
  - script: `scripts/compute_eval_metrics.py`
  - report: `evidence/reports/quantitative_eval_metrics.md`
- **Extended eval v1** (`51` cases across `4` documents — `2` English/Chinese
  papers + `2` Chinese markdown):
  - `46 / 51` pass (`90.2%`)
  - refusal precision `100%`, citation accuracy `88.4%`
  - `5` failures are honestly left as-is rather than prompt-tuned away
    (genuine retrieval misses on table single cells / abstract-implicit
    contributions / small md files)
  - manifest: `evidence/materials/EXTENDED_EVAL_V1.json`
  - scope: `evidence/materials/EXTENDED_EVAL_SCOPE.md`
  - report: `evidence/reports/extended_eval_v1_latest.md`

### Recent engineering hardening (2026-04-21)

- `ask` prompt now carries a structured `refused` field; `TaskService` has a
  dedicated `llm_refused` branch. This fixed a fabrication root cause.
- `RetrievalService` pins first-page chunk on author/affiliation/contribution
  queries to recover metadata intent.
- `scripts/predeploy_sanity.py` is the first pre-demo must-pass.

### Frontend UX polish (2026-04-21)

- evidence confidence bar (three-dot signal)
- clickable citation cards
- dedicated refusal card
- drag-and-drop upload
- hero button pulse animation
- `7 / 7` frontend smoke tests pass; build clean

### Judged submission assets

- `PPT_DECK_3PAGES_FINAL.md` + `VIDEO_SHOTLIST_5MIN_FINAL.md` source drafts
  exist.
- `deliverables/competition_kit/deck_3page_final.pdf` and
  `video_subtitles_5min_final.srt` baselines exist.
- Remaining open work is mostly last-mile asset production:
  - final native `PPT` (teammate task)
  - final edited `5`-minute video (teammate task)
  - full rehearsal on the target judging environment
  - screenshot refresh only if the target environment changes

## Review Constraints

Do not recommend broad pivots into:

- new task types
- OCR-heavy redesigns
- local-model branches
- public SaaS reframing
- large frontend redesigns

If you see stale historical contradictions, distinguish clearly between:

- current blocker
- stale artifact

Do not over-index on older warm-state-only `G3` language if newer strict `G3`
evidence is already present in the current bundle. Do not penalize the team
for keeping `5` extended-eval failures visible — that is an intentional
honesty choice (see `agent_handoff/SESSION_LOG.md` → memory entry
"评测诚实优先于刷分").

## What To Review

### 1. Whole-Project Judgment

- Is the whole project story clear, credible, and memorable?
- Does the current project deserve to be treated as near-freeze rather than as
  an unfinished prototype?
- If you had to summarize the project to a judge in one sentence, what would
  you say?

### 2. Product / Demo / Evidence Credibility

- Is the evidence-backed `ask` path strong enough to carry the judging story?
- Are the screenshots, replay reports, quantitative metrics, PDF back-link
  behavior, and refusal behavior convincing?
- Does the dual-layer evidence (strict G3 100% + extended 90.2%) strengthen
  or dilute the story? How should it be framed at judging time?
- Is anything still likely to damage trust in a live review?

### 3. Code / Architecture Risk

- Are there hidden implementation risks that still threaten demo credibility?
- Are the `llm_refused` branch and `metadata-intent` retrieval fallback
  coherent with the rest of `task_service.py` and `retrieval_service.py`?
- Is `scripts/predeploy_sanity.py` really enough as the pre-demo gate, or
  does it need broader coverage before judging day?
- If a current claim looks weak, point to the file evidence directly.

### 4. Submission Material Readiness

- Are the current materials internally aligned, especially the newly updated
  §7 of `HARD_EVIDENCE_SUMMARY.md` and the 量化指标 row in
  `SCORING_EVIDENCE_MATRIX.md`?
- Do the PPT/video baselines, technical write-up, platform proof, and
  evidence pages tell the same story?
- What still looks like draft mode rather than submission mode?

### 5. Final Readiness

- Based on current evidence, is each gate truly passed?
- What are the smallest remaining tasks before confident final submission?
- What should explicitly NOT be worked on now?

## Output Format

Use this exact structure:

### A. Top Findings

List the most important findings first, ordered by severity.
For each finding include:

- severity: `critical` / `high` / `medium` / `low`
- concise title
- why it matters
- file references
- concrete recommendation

### B. Overall Judgment

Give a blunt overall judgment of how close this is to a competition-strong
submission.

### C. Gate Assessment

State whether each gate is currently:

- `G1`: `pass` / `borderline` / `fail`
- `G2`: `pass` / `borderline` / `fail`
- `G3`: `pass` / `borderline` / `fail`

Keep the explanation brief and evidence-based.

### D. Completion Estimate

Give your own completion estimate (percentage or verbal) for each of:

- engineering / demo path
- evaluation rigor (strict G3 + extended 51-case)
- competition materials
- final submission readiness
- whole project overall

### E. Best Next Actions

Give the top 5 remaining actions with the highest leverage.

Separate them into:

- must-fix before judging
- should-fix if time allows
- should explicitly NOT be worked on now

### F. One Hard Truth

If the team is still making one important wrong assumption, state it
directly.

## Review Standard

Do not default to asking for more work. If something is already good enough,
say so explicitly. Focus on truth, risk, credibility, and judging impact.
