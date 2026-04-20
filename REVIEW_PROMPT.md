# External Review Prompt

Before writing your judgment, read these files first:

1. `PROJECT_CONTEXT.md`
2. `REVIEW_BUNDLE_INDEX.md`
3. `agent_handoff/FREEZE_FACT_SHEET_20260419.md`
4. `agent_handoff/TASK_BOARD.md`
5. `agent_handoff/PROJECT_HANDOFF.md`

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
- evidence and material consistency
- remaining high-leverage risks

Do not turn this into a generic SaaS roadmap review.

## Important Current Facts

- Runtime provider is already switched to `Wuwen Xinqiong`.
- Locked sample and locked prompt set already exist.
- Strict `G3` is now recorded as a fresh-upload three-run pass:
  - `evidence/experiments/20260420_g3_strict_rehearsal.md`
- Judge-facing proof pages are already assembled.
- Official `3`-page PPT and `5`-minute video source drafts already exist.
- Repo-native final production baselines already exist:
  - `deliverables/competition_kit/deck_3page_final.pdf`
  - `deliverables/competition_kit/video_subtitles_5min_final.srt`
- Remaining open work is mostly last-mile asset production:
  - final native `PPT`
  - final edited `5`-minute video
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
evidence is already present in the current bundle.

## What To Review

### 1. Whole-Project Judgment

- Is the whole project story clear, credible, and memorable?
- Does the current project deserve to be treated as near-freeze rather than as
  an unfinished prototype?
- If you had to summarize the project to a judge in one sentence, what would
  you say?

### 2. Product / Demo / Evidence Credibility

- Is the evidence-backed `ask` path strong enough to carry the judging story?
- Are the screenshots, replay reports, PDF back-link behavior, and refusal
  behavior convincing?
- Is anything still likely to damage trust in a live review?

### 3. Code / Architecture Risk

- Are there hidden implementation risks that still threaten demo credibility?
- Are the current architectural choices coherent for the stated scope?
- If a current claim looks weak, point to the file evidence directly.

### 4. Submission Material Readiness

- Are the current materials internally aligned?
- Do the PPT/video baselines, technical write-up, platform proof, and evidence
  pages tell the same story?
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

Give your own completion estimate for:

- engineering / demo path
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

If the team is still making one important wrong assumption, state it directly.

## Review Standard

Do not default to asking for more work. If something is already good enough,
say so explicitly. Focus on truth, risk, credibility, and judging impact.
