# 2026-04-20 Strict G3 Rehearsal

This note records the stricter `G3` batch executed after
`evidence/materials/STRICT_G3_EXECUTION_PLAN.md`.

## Evidence Boundary

- This file preserves the repo-verifiable parts of the strict run:
  - request ids
  - log-backed timestamps
  - `declared / retrieval_no_match` status
  - fresh-upload signals
  - fallback usage
- Operator-role and browser-state checklist items were handled offline during
  the live rehearsal and are summarized here without personal identity details.
- The three authoritative runs below are the final three fresh-upload success
  passes in `data/logs/call_logs.jsonl`.
- Two earlier fresh-upload success passes remain in the raw log as pre-final
  calibration and are not used as the main strict batch.

## Locked Setup

- Recorded date:
  - `2026-04-20`
- Log-backed run date in `UTC+08:00`:
  - `2026-04-19`
- Operator role:
  - second operator
- Machine:
  - local Windows workstation
- Runtime:
  - local frontend + local backend
- Locked sample:
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
- Locked path:
  - `upload -> ask -> citation -> PDF -> refusal`
- Active QA model:
  - `qwen3-235b-a22b-instruct-2507`
- Fallback screenshot set available:
  - yes (`evidence/screenshots/20260419_*`)
- Fallback used in the authoritative strict batch:
  - no

## Why This Is Stricter Than The Earlier Warm-State Note

- Each authoritative run has a different `file_id`, which is consistent with a
  fresh upload instead of reusing the already-loaded document state.
- Both answerable asks in all three authoritative runs have `cache_hit=false`.
- All answerable asks stay at `evidence_mode=declared`.
- All refusal asks stay on `retrieval_gate` with `retrieval_status=no_match`.
- No live request failed and no screenshot fallback was needed.
- The PDF jump/render step was part of the live checklist, but that click is
  not emitted into `data/logs/call_logs.jsonl`; the repo-verifiable portion is
  therefore the locked request sequence plus timestamps and request ids.

## Authoritative Runs

| Run | Local Start (`UTC+08`) | Local End (`UTC+08`) | Log-Backed Span | File ID | Q1 Declared | Q2 Declared | Refusal OK | Fallback Used | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `2026-04-19 18:00:39` | `2026-04-19 18:00:52` | `13.5s` | `3b33297c25444b7cb6a2b9466e53708a` | yes | yes | yes | no | fresh upload; both answerable asks uncached |
| 2 | `2026-04-19 19:25:50` | `2026-04-19 19:26:03` | `12.9s` | `3b988392fb9444da9d24e44111b4f6e3` | yes | yes | yes | no | fresh upload; both answerable asks uncached |
| 3 | `2026-04-19 19:36:59` | `2026-04-19 19:37:15` | `15.8s` | `3e72cb3f008047de962255ebcc68329f` | yes | yes | yes | no | fresh upload; both answerable asks uncached |

## Request IDs

- Run 1:
  - answerable 1: `1f959e23693e4e32acf49b460009ccd7`
  - answerable 2: `9bcd0f09b2bd407192ac8461c3a7423c`
  - refusal: `d44bfdfa4cdf4aec9adc90322ec942c4`
- Run 2:
  - answerable 1: `77cb7a1a6865446fa66df8d2f01dfc0c`
  - answerable 2: `808e42258ae545f9a1f0f2a33ef44549`
  - refusal: `04220964210d408596541371a6685ff1`
- Run 3:
  - answerable 1: `5363a0edc7074ef082148f84d6bda839`
  - answerable 2: `605fd2f0feae45c193379aba6a02723a`
  - refusal: `8ec726ccfb5c413ba62bb5e6599373d6`

## Log Cross-Checks

- Run 1:
  - Q1 latency: `4640 ms`
  - Q2 latency: `5998 ms`
  - refusal latency: `9 ms`
  - Q1 citations: `1`
  - Q2 citations: `2`
- Run 2:
  - Q1 latency: `4683 ms`
  - Q2 latency: `5083 ms`
  - refusal latency: `13 ms`
  - Q1 citations: `1`
  - Q2 citations: `2`
- Run 3:
  - Q1 latency: `6396 ms`
  - Q2 latency: `6325 ms`
  - refusal latency: `9 ms`
  - Q1 citations: `1`
  - Q2 citations: `2`

## Result

- `G3` pass / fail:
  - pass
- Strongest current wording:
  - strict `3`-run locked-path reproducibility pass on fresh uploads
- What improved versus the old note:
  - stronger than the earlier `20260419_g3_rehearsal_template.md` warm-state
    self-rehearsal because the authoritative batch no longer depends on a
    pre-loaded document state
- What this still does not prove:
  - it is judged-demo reproducibility evidence for the locked gold path, not
    open-domain product generalization proof

## Follow-Up Material Updates

- Update `evidence/materials/HARD_EVIDENCE_SUMMARY.md`
- Update `evidence/materials/PLATFORM_USAGE_EVIDENCE.md`
- Update `evidence/materials/QA_BRIEF.md`
- Replace residual warm-state-only wording in judge-facing source docs
