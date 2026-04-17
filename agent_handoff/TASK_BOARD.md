# Task Board

## Now

- No hard engineering blocker is currently open
- If preparing for judging/demo, prioritize presentation-path polish rather than feature work

## Next Best Tasks

1. ~~Demo-mode invite-code bypass~~ **DONE 2026-04-17** — `DEMO_MODE=true` env switch auto-creates sessions; invite form hidden in demo builds
2. ~~Soften stats panel for demo~~ **DONE 2026-04-17** — collapsed by default, single-line summary
3. ~~Add CSRF / origin validation for cookie-backed state-changing routes~~ **DONE 2026-04-17** — `OriginValidationMiddleware` rejects unsafe-method API requests whose Origin/Referer isn't in `CORS_ORIGINS`; missing-both passes (server-to-server)
4. Add expired-session cleanup script
5. Before 电赛 demo: set `DEMO_MODE=true` on deployed env and verify opening flow on staging URL

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
