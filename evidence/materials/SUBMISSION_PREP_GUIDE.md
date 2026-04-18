# Submission Prep Guide

## What This Is

This guide explains how to turn the current repository state into a clean
competition/demo submission package.

At the current stage, the locked gold-sample path is the primary submission
story. Broader replay outputs are secondary supporting material only.

## Recommended Submission Set

### Must-have

1. `PROJECT_ONE_PAGER.md`
2. `DEMO_SCRIPT_3MIN.md`
3. `GOLD_SAMPLE_RUNBOOK.md`
4. `COMPETITION_ASSET_PACK.md`
5. `evidence/reports/gold_sample_replay_real_summary_latest.md`
6. `evidence/reports/gold_sample_qa_compare_latest.md`
7. refreshed gold-sample screenshots

### Nice-to-have

1. `ARCHITECTURE.md`
2. `QA_BRIEF.md`
3. one experiment note for the locked gold-sample validation
4. optional stats-panel screenshot
5. optional backend API-docs screenshot

## How To Present The Project

### Product positioning

- A document assistant for paper/report reading and defense preparation
- Strongest differentiator is evidence-backed QA rather than generic generation

### Core value

- Upload document
- Parse structure
- Retrieve evidence
- Answer with citations
- Jump back to PDF evidence
- Refuse off-topic asks when retrieval does not match

### Why it is not a chat shell

- It preserves page-aware document structure
- It uses retrieval before answering
- It returns citations and evidence snippets
- It can jump back into the cited PDF page
- It logs replay evidence and comparison artifacts

## Suggested Demo Story

1. Show the locked gold-sample candidate
2. Run the first answerable ask
3. Open the cited PDF render
4. Run the second answerable ask
5. Run the off-topic refusal
6. Close with the replay summary and model decision

## Suggested Final Check Before Submission

- [ ] Locked prompts still match `GOLD_SAMPLE_CANDIDATE_20260418.json`
- [ ] `gold_sample_replay_real_summary_latest.md` is current
- [ ] `gold_sample_qa_compare_latest.md` is current
- [ ] The four gold-sample screenshots are current
- [ ] One-pager, demo script, and asset pack all use the same product positioning
- [ ] No broad-sample or historical provider artifact is being presented as the primary judging evidence
