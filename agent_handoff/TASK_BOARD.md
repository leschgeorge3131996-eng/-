# Task Board

## Now

- No hard engineering blocker is currently open
- Real Wuwen Xinqiong minimal-path validation is now done in-project
- A gold-sample candidate PDF plus `2 answerable + 1 refusal` candidate prompts are now locked
- If preparing for judging/demo, prioritize evidence refresh and material production rather than feature work

## Next Best Tasks

1. Refresh the real-only evidence pack around the locked gold-sample candidate:
   - ask result with citations
   - PDF evidence preview/render
   - refusal screenshot
   - candidate-set comparison report
2. Decide whether the existing replay/sample-report workflow should be updated to use the new session/access-token boundary and the locked candidate set
3. Add expired-session cleanup script
4. Before 电赛 demo: set `DEMO_MODE=true` on deployed env and verify opening flow on staging URL

## Recently Verified

- `2026-04-18`: `evidence/samples/chinese_llm_spatial_eval.pdf` completed the real path `upload -> ask -> citation -> PDF render` with `qwen3-235b-a22b-instruct-2507`
- `2026-04-18`: true off-topic ask (`木星有几颗卫星？`) refused correctly with `retrieval_no_match`
- `2026-04-18`: locked gold-sample candidate set in `evidence/materials/GOLD_SAMPLE_CANDIDATE_20260418.json`
- `2026-04-18`: `qwen3-235b-a22b-instruct-2507` and `qwen3-32b` both passed the candidate set; primary remains `qwen3-235b-a22b-instruct-2507`
- `2026-04-18`: replay tooling was updated to the current session/access-token boundary and refreshed `gold_sample_replay_real_*` outputs successfully

## Useful But Not Urgent

1. Detail-level replay comparison and report
2. Stronger grounding semantics for `summary` / `outline`
3. More polished competition materials

## Do Not Start By Default

1. New task types
2. OCR-heavy work
3. Local-model branch
4. Large frontend redesign
5. Public SaaS scope expansion

## Review Notes

- The strongest narrative remains:
  - evidence-backed document QA for paper/report reading and defense prep
- The weakest narrative remains:
  - generic document platform / open trial SaaS framing
- Refusal demos must use prompts that are purely off-topic; prompts that still mention in-document entities can retrieve and answer
- Current QA recommendation:
  - keep `qwen3-235b-a22b-instruct-2507` as default for stronger broad-answer grounding
  - keep `qwen3-32b` as validated fallback if demo/runtime latency becomes tighter
