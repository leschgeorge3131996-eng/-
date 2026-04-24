# Technical Optimization Roadmap — 2026-04-24

Scope: technical / end-to-end product work only. Non-technical materials such as papers, PPT, posters, and demo videos are explicitly out of scope for this roadmap.

## Consensus

Three parallel reviews looked at:

1. Backend RAG / retrieval / model invocation
2. Frontend UX / end-to-end demo stability
3. Evaluation / logs / deployment reliability

Consensus is strong:

- Do **not** switch the default QA model now. `qwen3-235b-a22b-instruct-2507` is the best completed full-suite candidate (`48/51`, `94.1%`) in `evidence/reports/model_selection_evaluation_20260424.md`.
- Do **not** rewrite the core path before judging/demo. The main path is stable enough and evidence-backed.
- The real technical ceiling is **retrieval + evidence localization**, especially table/parameter questions, same-meaning phrasing, and cross-page synthesis.
- The most useful near-term work is reliability and diagnosability: failure attribution, predeploy gates, front-end recovery, and targeted retrieval patches.

## Current Strengths

- Upload -> parse -> chunk -> retrieve -> ask -> structured evidence -> citation -> PDF preview is complete.
- Retrieval gate and LLM-level refusal protect against obvious hallucination.
- `TaskService` validates evidence quotes against selected chunks before declaring citation evidence.
- 51-case extended evaluation and 8-model quick screen now exist locally.
- Current model choice is evidence-backed, not guesswork.

## Main Technical Gaps

### 1. Retrieval Is Still Rule-Based

Current retrieval is centered around lexical scoring, IDF, bilingual hints, title bonus, and hand-built metadata intent fallback in `backend/app/services/retrieval_service.py`.

This is stable and easy to debug, but weak for:

- table cells
- numeric parameters
- same-meaning paraphrases
- implicit contributions
- cross-page synthesis

### 2. Table / Parameter Understanding Is Weak

Remaining failures include sample counts and Transformer parameter questions. These are often present in the document but not reliably retrieved or grounded because table structure is flattened into text chunks.

### 3. Evaluation Is Strong But Not Yet Diagnostic Enough

`scripts/extended_eval.py` scores pass/fail, page hit, declaration, and answer substring hit. It does not yet classify root cause into retrieval miss, wrong page, low confidence, model refusal, answer mismatch, or quote validation failure.

### 4. Runtime Observability Is Still Basic

Logs and summaries exist, but there is no automatic risk light for:

- P95 latency
- model errors
- refusal spike
- no-citation answers
- retrieval no-match spike
- disk/data retention risk

### 5. Frontend Is Still Synchronous

The current UX waits for a synchronous task response. This is acceptable for demo, but not ideal for slow models, flaky network, or repeated user clicks.

## Near-Term Priority Order

### P0 — Keep Demo Stable

Do these before any larger RAG rewrite:

1. Keep `MODEL_QA=qwen3-235b-a22b-instruct-2507` as default.
2. Keep `qwen3-next-80b-a3b-instruct` as fast fallback only if live latency becomes a blocker.
3. Keep `predeploy_sanity.py` as the must-run pre-demo gate.
4. Avoid turning on new retrieval architecture by default before it beats the current baseline.

### P1 — Failure Attribution Report

Enhance `scripts/extended_eval.py` so every failed case is tagged with a cause:

- `retrieval_miss`
- `low_confidence`
- `wrong_page`
- `undeclared_evidence`
- `answer_missing_expected_term`
- `model_refused`
- `quote_validation_failed`
- `model_or_network_error`

Why first: it tells us exactly whether the next patch should touch parsing, retrieval, context planning, prompting, or model routing.

### P2 — Table / Parameter Retrieval Patch

Target the remaining failure classes without changing the whole architecture:

- normalize table-like lines into `field: value` / `field=value` text
- add field aliases for common academic-paper parameters
- add query hints for `样本数`, `验证集`, `测试集`, `heads`, `layers`, `dropout`, `label smoothing`
- include neighboring chunks/pages when a query looks like parameter/table lookup

Goal: push the default model from `48/51` toward `50/51` without risking refusal precision.

### P3 — Frontend End-to-End Safety

Low-risk UX improvements:

- disable duplicate submits while task is running
- preserve question/file/result state on failure
- make retry obvious
- show explicit status for `declared evidence`, `candidate evidence`, `page found but no precise highlight`, and `no evidence`
- add friendly timeout copy rather than silent waiting

### P4 — Predeploy Gate Expansion

Extend `scripts/predeploy_sanity.py` beyond the 3 gold cases:

- health endpoint
- upload parse status
- ask result
- citation presence
- cited page fetch
- page render
- log write / summary read
- maybe disk/data-dir sanity

Output should be one final `READY` / `BLOCKED` risk light.

## Mid-Term Roadmap

### M1 — Hybrid Retrieval Prototype

Add an optional semantic retrieval path behind a flag such as:

```env
ENABLE_SEMANTIC_RETRIEVAL=false
```

Architecture:

1. current lexical retrieval remains primary and always available
2. embedding retrieval adds candidates
3. optional reranker scores merged candidates
4. existing evidence validation remains unchanged

This should first run offline against the 51-case suite. Only enable by default if it beats `48/51` without hurting refusal precision.

### M2 — Structured PDF / Table Pipeline

Extend parsing/chunk schemas to preserve:

- heading tree
- table rows/cells
- captions
- page number
- bbox / line mapping
- neighboring section context

This is the likely root fix for table and parameter questions.

### M3 — Async Task System

Change synchronous `/ask`, `/summary`, `/outline` into:

- create task -> return task id
- poll / stream task status
- support cancel / retry
- keep result recoverable after refresh

This is product-grade, but should wait until the judged/demo path is frozen.

### M4 — Runtime Monitoring

Build a minimal technical dashboard / risk report from `LogService`:

- success rate
- refusal rate
- no-match rate
- citation empty rate
- P50/P95 latency
- model error count
- cache hit rate
- top failure classes

## Recommended Next 3 Implementation Tasks

1. **Add failure attribution to extended eval**
   - Write cause tags into markdown and JSON.
   - Compare current 3 failures of the best model.
   - Use this as the next optimization dashboard.

2. **Patch table/parameter recall**
   - Add aliases and normalization for sample counts / parameters.
   - Re-run only affected cases first, then the 51-case suite.
   - Target `50/51` without reducing refusal precision.

3. **Add frontend task safety polish**
   - Duplicate-submit guard.
   - Retry and timeout copy.
   - Clearer citation/highlight state.
   - This is low risk and high demo value.

## Explicit Non-Goals For This Phase

- Do not replace the default model based on quick-screen results.
- Do not introduce a mandatory vector DB before a measured offline win.
- Do not rewrite PDF parsing before the failure attribution report confirms where it helps.
- Do not spend technical cycles on PPT/video/paper materials in this track.

## GitHub Note

Local commit `9834abe` exists for the model-selection work, but `git push` failed due to GitHub connection reset. The repo was still ahead of `origin/master` at the time this roadmap was written. Push should be retried when network is stable.
