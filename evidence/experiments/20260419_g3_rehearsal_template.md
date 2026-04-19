# G3 Rehearsal Template

Use this file when a second operator rehearses the locked judging/demo path.

## Goal

Prove the current demo environment is frozen and reproducible:

- second operator can follow the runbook
- `3` consecutive runs succeed
- each run stays within the practical demo window
- fallback behavior is defined ahead of time

## Setup

- Operator:
  - user self-rehearsal
- Machine:
  - local Windows workstation
- Environment:
  - local frontend dev server + local backend
- Demo mode enabled:
  - yes
- Warmup completed before timed runs:
  - yes
- Active QA model:
  - `qwen3-235b-a22b-instruct-2507`
- Fallback screenshot set available:
  - yes (`evidence/screenshots/20260419_*`)

## Timed Runs

| Run | Start Time | End Time | Duration | Answerable 1 Declared | Answerable 2 Declared | PDF Jump OK | Refusal OK | Fallback Used | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `2026-04-19 12:55:21` | `2026-04-19 12:56:17` | `56s` | yes | yes | yes | yes | no | same locked sample document; Q1 fresh, Q2 cache-warm, refusal normal |
| 2 | `2026-04-19 12:58:14` | `2026-04-19 12:59:21` | `67s` | yes | yes | yes | yes | no | repeated on the same loaded gold sample document |
| 3 | `2026-04-19 13:01:20` | `2026-04-19 13:01:44` | `24s` | yes | yes | yes | yes | no | repeated on the same loaded gold sample document |

## Request IDs

- Run 1:
  - answerable 1: `692bda1f05684649a9585d72e8e3901e`
  - answerable 2: `b552670d1e424225a2af7b36de0091dd`
  - refusal: `befcb8116ccf42a198f4f3ac6c1fc282`
- Run 2:
  - answerable 1: `8d41e5339676485194a8b17dd9fea760`
  - answerable 2: `f006c65103c94eb881aad9d4c40cdc80`
  - refusal: `f4375cb1829f49e7b52b21c52603cff4`
- Run 3:
  - answerable 1: `83e7f541e8204324b19d42d809152942`
  - answerable 2: `a4de68c753454a33b68388f99f0c9855`
  - refusal: `2768299a88054e8aa13427d91356a0be`

## Result

- `G3` pass / fail:
  - pass
- Main blocker if failed:
  - none
- Follow-up action:
  - move on to final material polish and final export bundle refresh
  - note for future stricter rehearsal: these three timed runs reused the already-loaded gold sample document after warmup; if a cold-start upload rehearsal is later required, run one additional operator pass from a fully fresh page state
