# Competition Plan V2

## Status

This file is the current execution baseline for competition preparation.

Until explicitly replaced, future optimization work should follow this plan first.

Created: `2026-04-18`

## Goal

- Primary goal: build a `national first prize`-level submission package for the `Wuwen Xinqiong` topic
- Secondary goal: if time or environment constraints appear, still keep the package strong enough for the national finals and topic-award line
- Main demo path: `ask -> citation -> PDF back-link -> refusal`
- Strategy: stop expanding product scope, focus on platform alignment, judge-proof evidence, stricter reproducibility, and submission completion

## Gold Sample Policy

- At the current stage, only lock a `gold-sample candidate`, not a final gold sample.
- The document candidate can be selected before platform migration is finished.
- The final gold sample question set and all official screenshots/material outputs must only be locked after:
  - `G1` real platform path is live
  - `G2` second-round validation passes after the provider switch
- Before `G2`, any demo questions are only `candidate questions`, not final official prompts.

## Go / No-Go Gates

### G1. Real platform path is live

Must pass before:

- formal material rewrites
- formal replay generation
- formal screenshot/video capture

Pass conditions:

- the project can complete at least one real `ask` request through `Wuwen Xinqiong`
- returned model/provider are from the target platform
- first platform screenshots and call records are collected

### G2. Second-round validation passes after provider switch

Must pass before:

- official demo screenshot capture
- video recording
- poster key visual finalization
- metrics table finalization

Pass conditions:

- fixed gold sample `2 answerable + 1 refusal` all pass
- citations are present for answerable cases
- citation can open PDF evidence
- at least one of `bbox` or `snippet` is stably visible
- refusal case is clearly rejected

### G3. Demo environment is frozen and reproducible

Must pass before:

- large-scale rehearsal
- final material lock

Pass conditions:

- a second teammate can run the main demo successfully using the runbook
- `3` consecutive successful runs
- each run stays within `3` minutes
- fallback to screenshots/recording is defined

## Current Workstreams

### 1. Platform Alignment

- validate `Wuwen Xinqiong` API externally
- switch the project main provider
- stabilize provider/model/request logging
- collect platform usage evidence

### 2. Gold Demo Path

- lock `1` Chinese gold-sample candidate PDF
- define `2` answerable candidate questions + `1` refusal candidate question
- re-upload and validate under the current parser path
- validate again after provider switch
- only after `G2`, promote the candidate set into the final gold sample
- reduce demo to the ask-only path

### 3. Real-Only Evidence

- define what is allowed into the competition evidence pack
- exclude mock and old-provider artifacts
- generate authoritative replay outputs and metric tables

### 4. Submission Materials

- technical paper
- `3`-page PPT
- `5`-minute video
- poster
- product/technical write-up
- platform usage page
- scoring-to-evidence mapping page
- final screenshot set

## Hard Rules

- Do not add new task types
- Do not pivot to OCR-heavy work
- Do not start a local-model branch
- Do not make `summary / outline` the main demo
- Do not do a large frontend redesign
- Do not treat old-provider materials as competition-ready artifacts

## Immediate Next Actions

1. Freeze the official submission spec crosswalk and score-to-evidence matrix
2. Lock the judge-facing platform usage page and hard-evidence summary
3. Keep only `real-only` evidence in the main judging path and push historical artifacts to appendix
4. Upgrade `G3` from warm-state rehearsal toward a stricter reproducibility pass
5. Finish the product/technical write-up, `3`-page PPT, `5`-minute video, and poster around the same locked gold-sample wording
6. Only after the main materials and reproducibility path are frozen, decide whether a judged-demo URL is worth the remaining time

## Notes

- Old materials may remain in the repo for history, but they must not be treated as competition-ready by default.
- If a later plan conflicts with this file, this file remains the active baseline until explicitly updated.
