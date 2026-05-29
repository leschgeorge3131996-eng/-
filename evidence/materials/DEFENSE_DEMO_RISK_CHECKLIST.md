# Defense Demo Risk Checklist

## Goal

Keep the live judged demo and defense inside the strongest verified path, and
recover cleanly if the target environment drifts.

## One-Line Claim

Use a sentence close to this one:

`We verified a reproducible evidence-backed ask loop on a locked paper sample:
upload a paper, answer with citations, jump back to cited PDF evidence, and
refuse off-topic asks.`

## Hard Boundaries

- Do not present the project as a generic document-chat platform.
- Do not present the project as a public SaaS/open ecosystem.
- Do not claim open-domain or arbitrary-PDF stability beyond the locked
  judged-demo path.
- Do not center `summary`, `outline`, login, invite codes, stats panel, or API
  docs in the main story.
- Do not improvise a new sample, new prompt, or new task type during a judged
  demo unless explicitly forced.

## Pre-Demo Must Pass

- [ ] Run `scripts/predeploy_sanity.py` on the demo machine; it archives
      `data/logs/call_logs.jsonl`, warms caches, and exits `0` only when
      all `3` gold cases pass end-to-end. Report lands at
      `evidence/reports/predeploy_sanity_<timestamp>.md`
- [ ] Run `GOLD_SAMPLE_RUNBOOK.md` once on the actual demo machine
- [ ] Use the locked sample PDF and the locked prompt set only
- [ ] Confirm answerable asks show citations and declared evidence
- [ ] Confirm the cited PDF page opens/render correctly
- [ ] Confirm the refusal stays `retrieval_no_match` with no citations
- [ ] Keep the latest screenshot set locally ready as fallback
- [ ] Keep the final PPT/video wording aligned with the same locked story

## Highest-Risk Failure Modes

### 1. Claim Drift

- Risk:
  - the operator starts saying the system is broadly stable for any document
- Why it hurts:
  - it overclaims beyond the current evidence and makes cross-examination easy
- Prevention:
  - keep the story at the locked judged-demo path and evidence-backed `ask`
- Recovery:
  - restate the boundary immediately:
    - reproducible on the locked paper sample
    - not pitched as arbitrary-document generalization

### 2. Asset Mismatch

- Risk:
  - PPT, video, screenshots, and proof pages describe different stories
- Why it hurts:
  - judges read this as "not actually frozen"
- Prevention:
  - keep all high-visibility assets on the same `upload -> ask -> citation ->
    PDF -> refusal` narrative
- Recovery:
  - switch to the primary judged-material path and stop referencing historical
    baselines

### 3. Runtime Drift

- Risk:
  - cold start, high latency, or a different machine/session causes the live
    path to wobble
- Why it hurts:
  - the project looks less controllable than the evidence pages suggest
- Prevention:
  - warm up on the actual machine before the judged slot
- Recovery:
  - switch to the latest locked screenshot set and keep the spoken story
    unchanged

### 4. Candidate Evidence Instead Of Declared Evidence

- Risk:
  - an answer appears, but the UI falls back to candidate context semantics
- Why it hurts:
  - it weakens the strongest selling point of the project
- Prevention:
  - confirm declared evidence during warmup
- Recovery:
  - do not improvise; switch to the screenshot pack and continue the same
    narrative

### 5. PDF Preview Failure

- Risk:
  - the answer cites pages but the PDF preview does not open cleanly
- Why it hurts:
  - the judge loses the most visual proof step in the chain
- Prevention:
  - verify PDF render in the warmup pass
- Recovery:
  - use the locked PDF-render screenshot immediately and continue

### 6. Operator Improvisation

- Risk:
  - changing the prompt, using a different paper, opening stats/API pages
    without being asked, or drifting into login/platform talk
- Why it hurts:
  - it expands the surface area and increases failure odds for no scoring gain
- Prevention:
  - follow the fixed runbook order
- Recovery:
  - stop the detour and return to the locked gold-sample path

### 7. Cold-Clicking The Live URL

- Risk:
  - to look "already deployed," the operator opens the Render free-tier URL
    live; it has slept (15-min idle) and cold-starts in ~30s, spinning in
    front of judges
- Why it hurts:
  - a public URL that hangs reads worse than a clean local demo, and it is a
    self-inflicted wound for no scoring gain
- Prevention:
  - the judged demo runs on the rehearsed local hot path, full stop
  - treat the live URL as supplementary evidence only ("deployed and
    reachable"): show it via a pre-warmed screenshot or QR code, and warm it
    by hitting the URL ~1 minute before any moment you might show it
- Recovery:
  - do not wait on the spinner; switch to the local path or the screenshot and
    keep the spoken story unchanged

## Live Demo Order

1. Load/upload the locked sample PDF
2. Ask the first answerable question
3. Show answer, citations, and the cited PDF page
4. Ask the second answerable question
5. Show the concise numeric answer with citations
6. Ask the refusal question
7. Close on why refusal matters for evidence-backed QA

## Fallback Rules

- If answerable output falls back to candidate/no-citation mode:
  - switch to the latest locked screenshot set
- If the PDF preview fails:
  - switch to the locked PDF-render screenshot
- If latency becomes too long:
  - stop waiting, switch to screenshots, and keep the same spoken script
- If a judge asks about broader stability:
  - cite the locked gold-sample reports first
  - describe broader replay only as secondary evidence

## Bad Answers To Avoid

- "It works for any PDF."
- "Summary and outline are equally grounded."
- "We are already a stable document platform."
- "The login/invite flow is one of the core innovations."

## References

- `evidence/materials/GOLD_SAMPLE_RUNBOOK.md`
- `evidence/materials/QA_BRIEF.md`
- `evidence/materials/FINAL_SUBMISSION_CHECKLIST.md`
- `evidence/reports/gold_sample_qa_compare_latest.md`
- `evidence/reports/gold_sample_replay_real_summary_latest.md`
