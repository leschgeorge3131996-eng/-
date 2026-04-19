# Session Log

Append-only log for both Codex and Claude Code.

Entry format:

```text
## YYYY-MM-DD / Agent
- Summary:
- Files touched:
- Verification:
- Open risks:
- Recommended next step:
```

## 2026-04-19 / Codex

- Summary:
  - Investigated the fresh Q2 instability reported during manual demo-mode testing: `作者最终的方法排名和总体准确率分别是多少？` was sometimes returning the correct answer text but falling back to `检索上下文 / candidate` even after cache clear
  - Confirmed the issue was real, not just stale cache: the cached ask payload itself contained `evidence_mode=candidate`, `used_chunk_ids=[]`, `evidence_quotes=[]`
  - Added a backend safety net in `TaskService`: when an `ask` turn has matched retrieval but missing structured evidence, the service now retries once internally before surfacing the result
  - Added logging/caching metadata `ask_evidence_retry_count` so future drift can be diagnosed from `call_logs.jsonl` and cache payloads
  - Added a regression test covering `plain text / no JSON on first ask -> declared JSON on second ask`
  - Restarted the local backend, cleared `data/cache`, and verified Q2 again through local demo-session upload/ask flow
  - Recorded a fresh stability check at `evidence/experiments/20260419_q2_declared_stability_check.md`: `3 / 3` fresh real runs returned `declared`, `2` used chunks, `2` evidence quotes, `2` citations, with the expected `第六 / 56.20%` answer
- Files touched:
  - `backend/app/services/task_service.py`
  - `backend/tests/test_services.py`
  - `evidence/experiments/20260419_q2_declared_stability_check.md`
  - `agent_handoff/CURRENT_STATUS_20260418.md`
  - `agent_handoff/SESSION_LOG.md`
  - `agent_handoff/TASK_BOARD.md`
  - `agent_handoff/PROJECT_HANDOFF.md`
- Verification:
  - backend tests: `55 passed`
  - local backend health after restart: `demo_mode=true`
  - local real Q2 ask:
    - request `70248bc85f3d4a90a148b74147f0649a`
    - `retrieval_status=matched`
    - `evidence_mode=declared`
    - `citation_count=2`
  - fresh Q2 stability requests:
    - `785bf35b11e5418f942a7e08d5b33351`
    - `1e38cbd263424988a1880bb286a20fcf`
    - `9df441cc64bc487aa90a59fc66275602`
- Open risks:
  - formal `G3` is still not passed until the operator checklist is completed and recorded
  - `model_client.py` still has historical prompt-string encoding debt; current fix avoided a risky prompt-file rewrite and instead hardened the service layer
- Recommended next step:
  - resume from formal `G3` rehearsal; the known Q2 evidence blocker is no longer the reason to hold it

## 2026-04-19 / Codex (G3 marked pass)

- Summary:
  - User completed the planned `G3` operator rehearsal on the locked gold sample flow
  - Recorded the three timed runs in `evidence/experiments/20260419_g3_rehearsal_template.md`
  - All three runs passed the same core checks:
    - answerable 1 declared
    - answerable 2 declared
    - PDF jump/preview confirmed
    - refusal remained `retrieval_gate / retrieval_no_match`
  - Marked `G3` as `pass` in the shared handoff files, with one explicit caveat: this was a warm-state repeatability pass on the same already-loaded document after warmup, not a stricter cold-start upload-from-zero rehearsal
- Files touched:
  - `evidence/experiments/20260419_g3_rehearsal_template.md`
  - `agent_handoff/CURRENT_STATUS_20260418.md`
  - `agent_handoff/PROJECT_HANDOFF.md`
  - `agent_handoff/SESSION_LOG.md`
  - `agent_handoff/TASK_BOARD.md`
- Verification:
  - run 1: `12:55:21 -> 12:56:17` (`56s`)
  - run 2: `12:58:14 -> 12:59:21` (`67s`)
  - run 3: `13:01:20 -> 13:01:44` (`24s`)
  - request ids logged for all `3 x 3` ask/refusal calls
- Open risks:
  - if a fully cold-start rehearsal is later required by another reviewer, one more upload-from-zero pass would still be useful
  - current top priority is no longer a feature or stability blocker; it is final competition asset polish/freeze
- Recommended next step:
  - refresh the final bundle and push materials toward final PPT / poster / video submission shape

## 2026-04-16 / Codex

- Summary:
  - Improved evidence semantics for `ask`
  - Improved PDF preview match states and page-specific snippet behavior
  - Added document access tokens, retention metadata, delete flow, and cleanup script
  - Added frontend smoke tests for key flows
  - Added invite-code trial sessions and document ownership
  - Moved session auth to `HttpOnly` cookie
  - Removed backend `X-Session-Token` fallback so cookie is the only session entry
  - Prepared external review bundle and review prompt
  - Created this shared `agent_handoff/` folder for future model handoff
- Files touched:
  - backend auth/session, file/task, and test files
  - frontend app/api/components/tests files
  - docs and evidence-facing review files
- Verification:
  - backend tests: `44 passed`
  - frontend smoke tests: `7 passed`
  - frontend build: passed
- Open risks:
  - no CSRF/origin validation yet for cookie-backed state-changing routes
  - stats panel may hurt demo/judging if noisy real metrics are shown live
  - invite-code login may add unnecessary demo friction if left visible in judging flow
- Recommended next step:
  - if demo/judging is the goal, polish presentation path first
  - if broader external testing is the goal, add CSRF/origin validation next

## 2026-04-17 / Claude Code

- Summary:
  - Softened the first-screen stats panel for demo: collapsed by default, single-line status summary (green dot "系统正常 · 已完成 N 次任务" / amber "运行中 · 有效 M / 总计 N" when errors exist) plus a "展开详情 ▾" toggle that reveals the original 6-card grid on click
  - Rationale: real 火山方舟 latency (p95 often 10s+) and any non-zero error count were flashing on first screen and risked hurting the judging impression; the panel now leads with a reassuring summary and preserves all numbers one click away
  - Chose not to pre-commit the existing dirty worktree before this change: only 3 frontend files are touched (`App.tsx`, `styles.css`), reversibility is via per-file checkout, and the handoff already marks the dirty state as expected
- Files touched:
  - `frontend/src/App.tsx` (added `statsExpanded` state; replaced the stats panel JSX)
  - `frontend/src/styles.css` (added `.stats-head`, `.stats-toggle`, `.stats-summary`, `.stats-dot` styles)
- Verification:
  - frontend smoke tests: `7 passed`
  - frontend build: passed (`tsc && vite build`, 598 modules)
  - backend tests: not run (no backend-side change)
- Open risks:
  - Judges who want to see live throughput/latency will need to click "展开详情"; if that feels like hiding, revert is one edit (set `useState(true)`)
  - Still no CSRF/origin validation on cookie-backed state-changing routes
  - Invite-code login remains visible on first screen — demo friction still unaddressed (TASK_BOARD "Next Best Tasks" #1)
- Recommended next step:
  - Decide whether demo mode should also bypass/hide invite-code login (TASK_BOARD #1)
  - Tighten one-sentence product positioning across README/first-screen subtitle/defense script

## 2026-04-17 / Claude Code (positioning pass)

- Summary:
  - Aligned the product one-liner across five first-impression surfaces to the canonical handoff positioning ("面向论文与报告阅读、答辩准备的文档助手；每一条回答都能跳回 PDF 原文证据")
  - Removed the prior "面向科研与智能办公场景的个人智能文档助理" framing from all five, because the handoff explicitly flags the "通用文档平台 / 个人助理" framing as the weakest narrative for judging
  - Did not touch `HERO_PILLS` (already reinforces "证据回链") or secondary sections like ONE_PAGER bullet fields / QA_BRIEF to avoid scope creep
- Files touched:
  - `frontend/src/App.tsx` (hero subtitle + `DEMO_DOCUMENT_CONTENT` opening line)
  - `README.md` (opening paragraph)
  - `evidence/materials/PROJECT_ONE_PAGER.md` ("一句话定义" sentence)
  - `evidence/materials/DEMO_SCRIPT_3MIN.md` (20s 开场 paragraph)
- Verification:
  - frontend smoke tests: `7 passed`
  - frontend build: passed (`tsc && vite build`, 598 modules)
  - backend tests: not run (no backend-side change)
- Open risks:
  - The new one-liner privileges `ask` as the hero; if demo emphasizes `summary` / `outline`, the opening may feel narrower than the live demo — keep ask-first in the demo flow
  - `PROJECT_ONE_PAGER.md` still contains "作品形态：个人智能助理" bullet and "端云协同" phrasing further down; not changed this round because they are below-the-fold structural fields, but if the one-pager is read top-to-bottom the reader may feel a tonal shift between the new one-liner and the older body
- Recommended next step:
  - Ask user whether to also rewrite PROJECT_ONE_PAGER body + QA_BRIEF opening for full tonal consistency
  - TASK_BOARD #1 (demo-mode invite-code bypass) is still the largest remaining demo-friction lever

## 2026-04-17 / Claude Code (UI polish round + end-of-day checkpoint)

- Summary:
  - User asked for visible UI polish, not a redesign. First pass was too subtle (gradient brandmark, citation-card left stripe, shimmer on primary button, layered panel shadows, global focus-visible) — user could not see a difference.
  - Two suspected causes: (a) changes were mostly hover/focus states, not first-glance, (b) frontend dev server wasn't running, so the browser was serving stale pre-build CSS.
  - Second pass added visible ambient layer: fixed-position blurred orbs on `.page::before` (warm terracotta, top-left) and `.page::after` (deep navy, bottom-right) with slow auroraDrift animation. First attempt was invisible because the `:root` background had competing radial-gradients at the same spots. Fix: stripped the `:root` radial-gradients down to a clean linear-gradient base, boosted orb opacity (0.78 / 0.62) and saturation. Orbs now dominate the ambient layer.
  - User feedback on brandmark: `clamp(48px, 7.4vw, 82px)` with `letter-spacing: -0.055em` was too large and too tight. Dialed back to `clamp(36px, 5vw, 58px)` with positive `letter-spacing: 0.1em` — CJK characters need positive tracking, not negative.
  - Also in this session: added new feedback memory "Proactive git commit + notify" per explicit user instruction — commit at natural break points without being asked, and tell the user; ask before pushing.
- Files touched:
  - `frontend/src/styles.css` (hero section, brandmark, page orbs, :root background, hero pills, eyebrow badge)
  - `agent_handoff/SESSION_LOG.md` (this entry)
- Verification:
  - frontend: `npm run build` passed twice this round (598 modules, ~24KB gzipped CSS); smoke tests `7 passed` on the preceding demo-mode commit
  - User has not yet visually confirmed the orbs/brandmark in the second pass — pending for next session
- Open risks:
  - Still no visual confirmation from the user that the second pass orbs are visible. If tomorrow they still don't see them, likely causes in order: (1) browser hard cache (Ctrl+F5 twice), (2) serving old dist/ via `start_yandatong.cmd`, (3) running on a different machine/deployment than expected.
  - Brandmark shimmer animation may feel busy if the page is otherwise still; if user dislikes movement, remove the `brandShimmer` keyframe call (keep the static gradient).
  - The eyebrow was restyled from a plain orange line of text into an uppercase pill with a pulsing dot; user has not confirmed they want that directional shift — it's more "SaaS landing page" than "paper reading tool".
- Recommended next step for tomorrow:
  - Confirm visually with the user that the orbs + brandmark look right on their screen before continuing. If yes, proceed to the next polish target: **result panel + answer rendering** (the second biggest demo eyeball magnet — currently still plain).
  - Specific candidates for round 3: animated skeleton while awaiting model response; upgrade the evidence-quote rendering (currently uses system serif fallback chain — may land on SimSun on Windows which looks dated); more dramatic entrance animation when a new result appears.
  - TASK_BOARD #3 (CSRF/origin validation) remains the outstanding security item; can be tackled between UI rounds.

## 2026-04-17 / Claude Code (demo mode: auto-session, no invite code)

- Summary:
  - User clarified context: this is an electronics competition (电赛), not a public alpha. Judges are a small trusted audience, so the invite-code gate adds pure demo friction with no real abuse-protection value.
  - Decision: keep the session/ownership plumbing intact (still need per-session document isolation), but remove the invite-code UI gate under a new `DEMO_MODE=true` env switch. Production alpha deploys with `DEMO_MODE=false` behave exactly as before.
  - Flow in demo mode: on first visit the frontend tries cookie-restore, falls back to `POST /api/auth/demo-session` which returns a new session with a `demo-xxxxxx` label. Zero clicks between opening the URL and uploading a document.
  - UI changes in demo mode: trial-boundary-card says "演示模式" + safer copy; "退出会话" button hidden (there is no logout concept when demo self-issues); if demo-session creation ever fails a friendly retry button appears instead of the invite-code form.
- Files touched:
  - `backend/app/core/config.py` (new `demo_mode` field)
  - `backend/app/services/auth_service.py` (extracted `_issue_session`, added `create_demo_session`, parameterized label prefix)
  - `backend/app/api/routes.py` (new `POST /auth/demo-session`; `/health` now returns `demo_mode`)
  - `backend/tests/test_api.py` + `backend/tests/test_services.py` (fixture `demo_mode=False`; two new tests — disabled-by-default returns 401, enabled issues cookie-backed session and advertises `demo_mode` on `/health`)
  - `frontend/src/api.ts` (`ensureDemoSession`, `fetchDemoMode`)
  - `frontend/src/App.tsx` (mount flow reads demo_mode first, then cookie-session, then auto demo-session; demo-mode-aware auth panel with retry)
  - `.env.example` (new `DEMO_MODE=false` with a comment block)
- Verification:
  - backend: `46 passed` (was 44, +2 demo-session tests)
  - frontend: smoke tests `7 passed`, `tsc && vite build` passed (598 modules)
- Open risks:
  - If `DEMO_MODE` is ever set to `true` on a public internet-exposed URL, anyone who finds the URL can upload docs and burn model tokens. Deploy DEMO_MODE=true only for the judging URL window.
  - `handleLogout` still exists but its button is hidden in demo mode; if someone wires another trigger to it, workspace clears and the user is dropped back to the "重新进入演示" retry card. Acceptable, but worth knowing.
  - Smoke tests still assert the invite-code form; if we later decide to default-enable DEMO_MODE, those tests need to mock `/health` to return `demo_mode=false` or be updated.
- Recommended next step:
  - Before the 电赛 demo: set `DEMO_MODE=true` in the deployed backend env and confirm the opening flow ("打开 URL → 立刻能上传") on the actual staging URL.
  - TASK_BOARD #3 (CSRF/origin validation) is the next logical security item; in demo-mode-only deployments it's even more important since the demo-session endpoint is unauthenticated.

## 2026-04-17 / Claude Code (one-pager body + QA brief + first commit)

- Summary:
  - Continued the positioning alignment into the one-pager body and the QA brief, so a reader going top-to-bottom sees consistent framing
  - ONE_PAGER "作品定位" bullets now say "面向论文与报告阅读、答辩准备的文档助手" / "受控 Alpha" / "论文精读、报告复核、答辩准备" (was "个人智能助理" / generic "智能办公")
  - ONE_PAGER 差异点 #4 dropped "统计面板" as a selling point (aligned with the softened first-screen stats panel this same session)
  - QA_BRIEF Q1 opening rewritten to the canonical one-liner; Q4 技术亮点 list also dropped "统计面板"
  - Committed the six clean files this session produced to local git as one `docs: ...` commit; deliberately left `frontend/src/App.tsx` and `frontend/src/styles.css` out because they still carry pre-session uncommitted auth/session/evidence changes that belong in a separate future commit
- Files touched:
  - `evidence/materials/PROJECT_ONE_PAGER.md` (作品定位 bullets + 差异点 #4)
  - `evidence/materials/QA_BRIEF.md` (Q1 opening + Q4 list)
  - `agent_handoff/SESSION_LOG.md` (this entry)
- Verification:
  - docs-only changes; no code path touched
  - frontend smoke/build not rerun this sub-round
- Open risks:
  - The stats-panel softening and hero subtitle change still live only in the working tree; any future `git checkout -- frontend/src/App.tsx frontend/src/styles.css` would lose them along with the older dirty work
  - ONE_PAGER 第三阶段/技术路线章节仍带"端云协同"技术词，没动，因为属于技术路线而非产品定位，保留合理
- Recommended next step:
  - If the user wants a fully clean commit history, next round do hunk-level staging on `App.tsx` / `styles.css` to carve out just the stats-panel + subtitle changes
  - Otherwise, TASK_BOARD #1 (demo-mode invite-code bypass) is still the biggest demo-friction lever left

## 2026-04-17 / Claude Code (result panel polish: loading skeleton + empty state)

- Summary:
  - Followed yesterday's recommended next step. The longest dead-air moment in a demo is the 5-10s model wait; previously the UI was a single plain sentence "模型处理中，首次请求可能需要 10 到 40 秒。" in a white card.
  - Replaced with a full shimmer skeleton that mimics the result layout: a status pill with a pulsing accent dot + the live load message, three badge-shaped shimmer pills, a 2x2 meta-card grid, and a dark terminal shell with six shimmering output lines. Judge sees motion + structural preview instead of waiting.
  - Also upgraded the empty state (first-visit, no result yet): previously a bland sentence, now a centered glyph (layered radial + ring + glowing dot with a gentle 3.4s drift animation) + bold title "等待你的第一次提问" + hint line. Bordered dashed card with a soft accent radial wash at the top.
  - Added `@media (prefers-reduced-motion: reduce)` guard to disable all four animations (skeleton shimmer, status-pill pulse, terminal-line shimmer, empty glyph drift).
  - Committed as `99abfdd` — the only uncommitted items left are the two untracked review bundle files (`REVIEW_BUNDLE_INDEX.md`, `REVIEW_PROMPT.md`), which are external-review artifacts and belong separately.
- Files touched:
  - `frontend/src/components/ResultPanel.tsx` (replaced loading branch and empty branch in the AnimatePresence block)
  - `frontend/src/styles.css` (new: `@keyframes skeletonShimmer/skeletonPulse/emptyGlyphDrift`, `.result-skeleton`, `.skeleton-status`, `.skeleton-pulse`, `.skeleton`, `.skeleton-badges/badge`, `.skeleton-meta-grid/card`, `.skeleton-terminal*`, `.empty-state*`, reduced-motion media query)
  - `agent_handoff/SESSION_LOG.md` (this entry)
- Verification:
  - frontend smoke tests: `7 passed` (tests don't assert loading copy, so the redesign is safe)
  - frontend build: passed (`tsc && vite build`, 598 modules, CSS 27.99 KB / 6.53 KB gzip — was ~24 KB, +~4 KB is the new skeleton/empty-state block)
  - backend tests: not run (no backend-side change)
  - User has not yet visually confirmed the skeleton/empty-state on their screen — pending. Dev server was not running when checked (`tmp_vite_public_*.log` empty, no vite/node processes). User will need to `cd frontend && npm run dev` and hard-reload (Ctrl+F5) to see the change; `start_yandatong.cmd` may serve `dist/` which is now rebuilt.
- Open risks:
  - The terminal-shell skeleton is dark and the surrounding page is warm beige — the visual jump from page to skeleton is deliberate (it previews the real terminal output) but may feel heavy for users who expect an all-light skeleton. If user wants it lighter, swap the `.skeleton-terminal` gradient to a light tone.
  - The empty-state glyph is subtle; on small panels it may look decorative-only. If user wants it more explicit, replace the three-span glyph with an inline SVG of a page + magnifying glass or similar.
  - Pulsing dot + drifting glyph + shimmer all run simultaneously; combined they may feel busy to motion-averse viewers, though each one individually is gentle and the reduced-motion media query disables them.
  - TASK_BOARD #3 (CSRF/origin validation) still outstanding; not addressed this round.
- Recommended next step:
  - Wait for user visual confirmation before pushing further UI changes. If good, candidate round-4 targets in priority order: (a) entrance animation for new result cards (stagger badges → meta → terminal → citations), (b) result-complete "ding" micro-interaction (flash border, or single pulse on status dot transitioning green), (c) citation-card entrance stagger when many evidence items appear.
  - If UI momentum stalls, pivot to TASK_BOARD #3 (CSRF/origin validation for cookie-backed routes) — security item that grows more important now that demo-mode session is unauthenticated.

## 2026-04-17 / Claude Code (result panel: staggered reveal + terminal sweep)

- Summary:
  - User confirmed previous round OK ("效果还可以"), so kept UI momentum. Problem: previous round fixed the wait (skeleton) but the payoff moment — when the real result appears — was still "everything pops simultaneously", wasting the narrative high point of the demo.
  - Rebuilt the result branch of `ResultPanel.tsx` so each section animates in on a timeline: badges 40ms → meta grid 120ms → evidence-state card 200ms → status/warning/token lines 240–300ms → citations container 340ms → first citation card 400ms (each subsequent +50ms) → evidence-quotes container 420ms → terminal shell 500ms. Each section uses the existing `revealMotion(delay)` helper (opacity 0→1, y 14→0, 280ms cubic-bezier(0.22,1,0.36,1)).
  - Changed `renderEvidenceCard` / `renderEvidenceQuote` signatures to accept a `baseDelay` param. Citation cards previously started their per-index stagger from 0ms regardless of container state — they were flashing in before badges. Now they inherit 0.4/0.48 base so they arrive after their container reveal.
  - Terminal shell gets a new `.terminal-shell-sweep` modifier class that adds a `::before` pseudo-element: a 2px-tall warm-accent horizontal gradient that sweeps left-to-right once (1.1s after a 0.55s delay) — the "model has answered" visual cue. Uses `animation: ... 1 both` so it decays to transparent and doesn't loop.
  - Reduced-motion media query disables the sweep; base reveal motion uses small distances (14px y) so it's tolerable even without motion, but `revealMotion` itself doesn't honor reduced-motion — candidate follow-up if anyone flags it.
- Files touched:
  - `frontend/src/components/ResultPanel.tsx` (wrapped each result section in `motion.div` with `revealMotion(delay)`; added `baseDelay` param to card/quote renderers)
  - `frontend/src/styles.css` (added `.terminal-shell-sweep::before`, `@keyframes terminalSweep`, and reduced-motion guard; made `.terminal-shell` position:relative)
  - `agent_handoff/SESSION_LOG.md` (this entry)
- Verification:
  - frontend smoke tests: `7 passed`
  - frontend build: passed (`tsc && vite build`, 598 modules, CSS 28.60 KB / 6.67 KB gzip — was 27.99 KB, +~0.6 KB is the sweep block)
  - backend tests: not run (no backend-side change)
  - User has not yet visually confirmed; dev server still not observed running. Hard-reload (Ctrl+F5) after `npm run dev` to see it.
- Open risks:
  - Total reveal takes ~780ms end-to-end (last card around 500ms + its own 280ms fade). For short answers with 1 citation this feels cinematic; for long answers with 8+ citations the tail is ~900ms which may feel slow if a judge is scanning fast. If flagged, tighten `renderEvidenceCard` per-index delta from 0.05 to 0.03.
  - The terminal sweep fires once on mount of `.terminal-shell-sweep`; if React re-renders the shell (e.g. copy button state change triggers a re-render that doesn't remount), the sweep won't replay — that's actually the intended behavior (one-time "done" flourish) but means the sweep only plays on fresh result arrival.
  - The sweep color is warm terracotta to match brand accent. On the dark terminal background it reads as "here's your answer" energy; if user wants a cooler/greener "success" feel, swap the gradient stops to `var(--success)` (#1f6a4e-ish range).
- Recommended next step:
  - Pause for user visual check. If the reveal feels too slow, tighten deltas. If it feels right, remaining UI lever is **markdown rendering inside the terminal** — currently plain; candidates: code-block syntax color, blockquote styling for quoted evidence, table polish. But that only matters if real demo answers use markdown, which should be verified against actual task outputs before spending effort.
  - Non-UI backlog unchanged: TASK_BOARD #3 (CSRF/origin validation), #4 (expired-session cleanup script), #5 (pre-demo DEMO_MODE verification on staging).

## 2026-04-17 / Claude Code (markdown polish: GFM + table/heading/task-list styling)

- Summary:
  - Executed the previous round's recommended next step after verifying the demo actually produces markdown: `outline` task's system prompt explicitly asks for "层级提纲"; `summary` asks for "结构化摘要". Both land inside the `.terminal-shell` via `MarkdownResult`, which until now only shipped `react-markdown` + `rehype-sanitize` — no GFM, so any `|` table the model emitted rendered as raw pipes and any `- [ ]` checklist rendered as literal brackets.
  - Added `remark-gfm` (18 packages) and wired it into `MarkdownResult` alongside a `table` component wrapper that scopes horizontal overflow to a `.markdown-table-wrap` container (prevents the table from blowing out the terminal shell on narrow viewports).
  - Added styling for six previously-bare surfaces inside `.rendered-markdown`: (1) small vertical accent bar before `h2`/`h3` (brand gradient, 3×0.85em), (2) list markers tinted — `ul` uses terracotta accent-deep, `ol` uses navy bold, (3) task-list checkboxes use `accent-color: var(--accent-deep)` and are negative-margin aligned with the text, (4) `hr` becomes a soft center-fade line instead of a hard border, (5) `strong` becomes navy 650 weight so bolded key terms stand out against ink-strong body text, (6) `del` (GFM strikethrough) becomes muted with a soft underline.
  - Tables: rounded 12px card wrap, subtle 1px borders, light header row, 0.5×0.8em cell padding, last-row border removed, terracotta-tinted row hover. The hover is 4% alpha so it doesn't scream; it's a "this row is live" hint, not a selection state.
- Files touched:
  - `frontend/package.json` + `frontend/package-lock.json` (added `remark-gfm`, 18 transitive packages)
  - `frontend/src/components/MarkdownResult.tsx` (`remarkPlugins={[remarkGfm]}`; `table` component override for overflow wrapping)
  - `frontend/src/styles.css` (new block appended after `.rendered-markdown pre code` — ~80 lines of heading/list/task/hr/strong/del/table rules)
  - `agent_handoff/SESSION_LOG.md` (this entry)
- Verification:
  - frontend smoke tests: `7 passed`
  - frontend build: passed (`tsc && vite build`, 689 modules — was 598, +91 from remark-gfm tree; CSS 29.95 KB / 6.94 KB gzip — was 28.60 KB, +1.35 KB from the new block)
  - backend tests: not run (no backend-side change)
  - Not yet visually confirmed by user; to see table/checklist styling they need a task output that actually contains a markdown table or a task list, which depends on the model's choice that run.
- Open risks:
  - `rehype-sanitize` default schema may strip some GFM-emitted HTML; quick spot-check says tables and task lists survive, but if a model emits HTML inside a table cell it may get cleaned. Trade-off is acceptable — prefer XSS safety over HTML passthrough.
  - Bundle jumped 598 → 689 modules because of GFM's micromark extensions. CSS +1.35 KB, JS bundle likely +~20 KB gzipped (not separately measured). For an alpha/demo build this is fine; if future bundle budgets tighten, consider dynamic-importing `MarkdownResult`.
  - The `h2`/`h3` accent bar is inline-block before the heading text — if a heading wraps to two lines, the bar stays next to the first character of the first line (that's the expected visual). On the off chance a model emits an `h1`, it won't get the bar — by design, h1 should feel like a title, not a section marker.
  - Task-list checkbox negative margin (`-1.15em`) assumes the default `react-markdown` GFM output wraps the checkbox inside the `li`. If GFM output format changes in a future `remark-gfm` major, the alignment may drift — low probability.
- Recommended next step:
  - Pause for user to run a live outline/summary task and confirm tables + checklists + headings look right. If they do, UI polish momentum can stop here (returns are diminishing — first-screen, result panel skeleton, staggered reveal, markdown all covered).
  - Next highest-value lever is **TASK_BOARD #3 (CSRF / origin validation)** — cookie-backed state-changing routes are the one remaining security debt that matters under `DEMO_MODE=true`.
  - TASK_BOARD #5 (deploy `DEMO_MODE=true` on staging and verify opening flow) is still the pre-demo must-do — no code work, but the checklist item belongs to whoever owns the deploy environment.

## 2026-04-17 / Claude Code (CSRF: Origin/Referer validation middleware)

- Summary:
  - Closed TASK_BOARD #3. Cookie-based sessions (now the only session entry after the X-Session-Token removal earlier in this codebase) are inherently exposed to CSRF: any third-party origin can trick a logged-in user's browser into issuing `POST /api/upload` / `POST /api/ask` / `DELETE /api/files/...` that rides the session cookie. `SameSite=Lax` blocks most drive-by GET-to-POST tricks but is not a complete defence (top-level form POSTs still attach the cookie; browser bugs happen). The OWASP-recommended next layer is Origin/Referer validation, which is what this round adds.
  - New `OriginValidationMiddleware` (in `backend/app/core/csrf.py`): on every non-safe method (`POST/PUT/PATCH/DELETE`) targeting the `/api` prefix, it parses the request's `Origin` header (falls back to `Referer` if Origin is missing or literal-`null`), normalizes it to `scheme://host[:port]`, and checks membership in a normalized allowlist derived from `settings.cors_origins`. Mismatch → `403 FORBIDDEN_ORIGIN` with a structured error body (goes through the same `ApiResponse` shape as the rest of the API).
  - Deliberate policy: **if both Origin and Referer are absent, the request passes**. Rationale: CSRF requires a browser to attach the victim's cookie, and every modern browser emits at least one of those two headers on state-changing requests. Server-to-server clients (TestClient, curl without `-e`, backend cron) legitimately omit both and blocking them would break tests and internal tooling without gaining real security — an attacker without a browser also can't steal the cookie in the first place. This matches Django's CSRF middleware posture.
  - Also deliberate: Origin header with literal value `"null"` (from sandboxed iframes or `file://`) is treated as absent and falls through to the Referer check. If neither is trustworthy, the request is rejected. Don't ever bless `null`.
  - Middleware registered **after** CORS in `main.py` so that at the runtime call order: CORS wraps CSRF wraps router. This means CORS handles `OPTIONS` preflights (which my middleware already explicitly passes through via the `SAFE_METHODS` set, but CORS handles them definitively without reaching me). Reject path still gets proper JSON body from the existing error envelope — CORS doesn't interfere with 4xx responses.
  - Allowlist reuses `CORS_ORIGINS` because they mean the same thing ("trusted frontend hosts"). Introducing a second env var would have let them drift out of sync, which is a worse failure mode than a shared one.
- Files touched:
  - `backend/app/core/csrf.py` (new — middleware + `normalize_allowed_origins` helper + `_origin_from_url` parser that collapses default ports to scheme-only form)
  - `backend/app/main.py` (imports `OriginValidationMiddleware`; registers it before CORS middleware so that in the final wrapped stack CORS is outermost)
  - `backend/tests/test_api.py` (+7 tests: no-headers pass, allowed Origin passes, foreign Origin rejected with FORBIDDEN_ORIGIN, foreign Origin rejected before logout even with a valid cookie + confirms session survives, Referer fallback works both ways, `Origin: null` rejected, GET is never gated)
  - `.env.example` (added comment block on `CORS_ORIGINS` explaining it now also gates CSRF)
  - `agent_handoff/TASK_BOARD.md` (marked #3 done)
  - `agent_handoff/SESSION_LOG.md` (this entry)
- Verification:
  - backend tests: `53 passed` (was 46, +7 CSRF tests all green)
  - frontend smoke tests: `7 passed` (uses mocked fetch so Origin check doesn't affect it; but this also means the smoke tests do NOT exercise the live CSRF path — that's covered by the backend tests)
  - Manual cross-check: `grep` confirms every POST/DELETE route handler in `routes.py` now sits behind the new middleware because the middleware is registered at the app level and the prefix filter (`/api`) matches the router mount point.
- Open risks:
  - **Deploy-time footgun**: if someone deploys the backend with `CORS_ORIGINS=http://localhost:5173` but the real frontend is served from e.g. `https://yandatong.example.com`, every write request from the browser will 403. The env-example comment warns about this, but the failure mode is "feature looks broken" not "feature is insecure", so it's self-correcting in practice. Still: demo-day deploy checklist should include verifying `CORS_ORIGINS` matches the actual frontend host.
  - **Referer header may be absent for privacy-stripping browsers** (e.g. Safari with Intelligent Tracking Prevention on cross-site navigations, `Referrer-Policy: no-referrer`). In that case, if Origin is also missing, the request passes. This is the "no-both" carve-out. For a browser to hit this path and attack us, the attacker's page would need to successfully strip *both* — which requires the victim to opt into an unusual policy. Acceptable risk for an alpha tool.
  - **No CSRF token layer**: I did not add a double-submit token or synchronizer token. OWASP's 2024 CSRF cheatsheet says Origin validation + SameSite is sufficient when both are correctly configured, and adding a token creates real complexity (frontend has to fetch/attach on every request; rotation on login/logout; failure modes around HMR). If we later expose the API to third-party clients (non-browser), we may want to revisit.
  - **Middleware does NOT check path beyond prefix**: any `/api` POST route gets guarded, present or future. Good for new routes, but means if someone later mounts a non-API POST endpoint under `/api/webhook/<provider>` that needs to accept external callbacks, they'll have to carve out an exemption. Flag for future me: there is currently no such endpoint.
- Recommended next step:
  - Pre-demo verification (TASK_BOARD #5): on the staging URL, set `DEMO_MODE=true` AND set `CORS_ORIGINS` to the deployed frontend host; confirm (a) a fresh visit can auto-create a session and upload, (b) any state-changing POST from a non-allowed origin returns 403. Lightweight smoke: open browser devtools and run `fetch('/api/upload', {method: 'POST', credentials: 'include'})` from a different-origin tab — should 403.
  - Remaining TASK_BOARD backlog: #4 (expired-session cleanup script) is the lowest-risk cleanup item; useful but not demo-critical.
  - Non-backlog candidate: revisit rate-limiting on `/api/ask` and `/api/upload` now that demo-mode makes unauthenticated session creation trivial — someone who figures out the URL can burn model tokens. Not blocking demo (shared IP + small audience) but worth noting.

---

## 2026-04-17 — PDF.js inline viewer attempt → reverted

### Motivation
Tester feedback: the side 文本定位 aside duplicates effort; the highlight should live inside the PDF itself. Agreed to try 档 1 (search-based highlight via PDF.js find controller) before the heavier 档 2 (bbox rectangles).

### What was built (commits f369743 + 19fcef2)
- New `frontend/src/components/PdfViewer.tsx`: wraps pdfjs-dist `PDFViewer + PDFFindController + EventBus`; load document once per src; page switch via `currentPageNumber`; highlight via `find` event on `textlayerrendered`.
- `PdfPreviewPanel.tsx`: dropped aside + `fetchDocumentPage` plumbing; header "已在 PDF 中高亮证据" chip.
- `App.tsx`: removed `page` from `buildFileContentUrl(...)` call so src is stable (avoids full document reload on page switch).
- `styles.css`: single-column `.pdf-preview-body`; `.pdf-frame-wrap` 78vh scroll container; `.pdfjs-host .textLayer .highlight` overlay; later added `color-scheme: only light !important` to `:root` to fight pdf_viewer.css globals.
- `App.smoke.test.tsx`: `vi.mock("./components/PdfViewer")` stub exposing `data-page`/`data-highlight`; removed `fetchDocumentPage` assertions; removed iframe-src assertion.

### Why it was reverted (commits 6e9c9e0 + 433535b)
Tested against a real Chinese academic PDF (tables + mixed layout):
1. **Highlight hit rate was poor.** Find controller searches the text-layer substring; on CJK text with column/line-break artifacts, the 40-char query rarely matched. User saw "已在 PDF 中高亮证据" chip but zero yellow on the page. This was the exact limitation I flagged when proposing 档 1, but the miss rate in practice was worse than estimated — the feature was effectively nonfunctional on the target corpus.
2. **Visual clash with ambient orbs.** The previous iframe was opaque; the pdfjs scroll container let the `.page::before / .page::after` radial gradients bleed through the preview area. Reported as "一坨莫名其妙的球".
3. **Globals pollution.** `pdf_viewer.css` sets `color-scheme: light dark` at `:root`; on a dark-mode-preferring OS that made native form controls render dark (invisible input text, grey upload button). Patched with `!important` override, but the fact that a viewer CSS file needed `!important` to neutralize is itself a smell.
4. **Ratio of cost to payoff.** 1.2MB worker bundle + CSS variable pollution + new dep + test-mocking indirection, for a feature that doesn't reliably deliver on this corpus. Reverting is cheaper than patching.

### End state
- Two git reverts on master (`6e9c9e0`, `433535b`).
- `pdfjs-dist` uninstalled (`npm uninstall` — package.json/lock already matched post-revert state, so no tracked diff).
- Tests: 7/7 frontend smoke tests passing; typecheck clean.
- UX restored to the prior iframe + side 文本定位 panel, which the user already accepted as a working baseline.

### If we want to retry later
Skip 档 1. Go straight to **档 2 (precise bbox)**:
- Backend: during chunking, store each chunk's bbox per page using PyMuPDF's `page.get_text("dict")` or `search_for(snippet)`.
- API: include `[{page, bbox}]` in the citation payload.
- Frontend: keep the iframe viewer, overlay an absolutely-positioned transparent div per citation page scaled to the rendered PDF's dimensions, draw highlight rectangles at the stored bbox coordinates.
- Cost: ~1–2 days, but it's 100% reliable and doesn't need pdf.js integration.

### Lesson for future rounds
Search-based highlighting is a dead-end for CJK academic PDFs. Don't revisit it. If the user asks for in-PDF highlight again, go straight to bbox overlays.

---

## 2026-04-17 — PDF bbox-based in-PDF highlight (档 2) shipped

**Author:** Claude (Opus 4.7)

Follow-up to the same day's 档 1 revert. Built the bbox overlay approach end-to-end.

### Backend
- `backend/requirements.txt`: added `pymupdf==1.27.2.2`. Kept `pypdf==5.9.0` (other code paths may still import it, and removal is out of scope).
- `backend/app/schemas/document.py`: new `BBoxRegion { page, x0, y0, x1, y1 }`, new `ParsedBlock { text, bbox }`, `ParsedPage` gains `width/height/blocks` (defaults 0/0/[] → old `.pages.json` still loads), `ParsedChunk` gains `bbox_regions` (default []).
- `backend/app/schemas/task.py`: `Citation` gains `bbox_regions: list[BBoxRegion] = []`.
- `backend/app/services/document_parser.py`: replaced pypdf-based `_read_pdf` with PyMuPDF. For each page, iterates `page.get_text("blocks")`, keeps text blocks only (`block_type == 0`), normalizes text, sorts by `(y, x)`, stores per-block bbox. Falls back gracefully if pymupdf is missing (ParseError).
- `backend/app/services/chunk_service.py`: new `_chunk_from_blocks(page)` path that merges blocks into chunks while accumulating their bboxes. Non-PDF (`page.blocks == []`) keeps the old text-based flow with `bbox_regions=[]`. `_merge_small_chunks` concatenates bbox lists when merging.
- `backend/app/services/task_service.py` `_build_chunk_ref`: threads `chunk.bbox_regions` into Citation.
- `backend/app/services/file_service.py`: new `render_document_page(file_id, page_number, dpi=144)` returns PNG bytes via `pymupdf.open(...).get_pixmap(dpi=...).tobytes("png")`.
- `backend/app/api/routes.py`: new endpoint `GET /api/files/{file_id}/pages/{page_number}/render?dpi=144` → `image/png`. Existing `/pages/{n}` now also returns `width` and `height`.

### Frontend
- `frontend/src/types.ts`: added `BBoxRegion`; `Citation.bbox_regions?`; `DocumentPageData.width/height?`. Removed now-unused `PdfPreviewMatchState`.
- `frontend/src/api.ts`: added `buildPdfPageRenderUrl(fileId, page, token, dpi=144)` + exported `PDF_PAGE_RENDER_DPI`.
- `frontend/src/components/ResultPanel.tsx`: `onOpenPdfPage` signature now takes the full `Citation` instead of `(pages, snippet)`.
- `frontend/src/App.tsx`: new `previewBboxes` state (reset alongside `previewSnippet` in all 5 reset sites); on "打开定位" click, stores citation.bbox_regions; passes `bboxRegions={previewBboxes.filter(r => r.page === previewPage)}` to the panel. Dropped the `src` prop (panel builds its own render URL). Removed unused `buildFileContentUrl` import.
- `frontend/src/components/PdfPreviewPanel.tsx`: full rewrite. Gone: iframe + text aside + sentence highlight. In: `<img src={renderUrl}>` wrapped in `.pdf-render-wrap > .pdf-render-inner` (relative) with an absolute `.pdf-highlight-layer` of transparent bbox rectangles scaled by `renderedSize / nativeDimensions`. `nativeDimensions` comes from `fetchDocumentPage` (`page.width/height`) with a fallback of `imgNaturalSize * 72/144` for old docs that predate the width/height fields. `fetchDocumentPage` is still called so the existing smoke test (`toHaveBeenCalledWith("file-pdf", 2, "token-pdf")`) still holds.
- `frontend/src/styles.css`: removed `.pdf-preview-body`, `.pdf-frame-wrap`, `.pdf-frame`, `.page-text-*`, `.page-text-highlight`, and their `@media` overrides. Added `.pdf-preview-status`, `.pdf-render-wrap` (flex centering, 82vh max-height, scroll), `.pdf-render-inner` (relative, shrink-to-image), `.pdf-render-image`, `.pdf-highlight-layer` (absolute inset:0), `.pdf-highlight-rect` (translucent accent-deep fill + border, `mix-blend-mode: multiply`).
- `frontend/src/App.smoke.test.tsx`: updated the preview-frame src assertion from `#page=5` (iframe hash) to `/pages/5/render` (new render endpoint). Test cast changed from `HTMLIFrameElement` to `HTMLImageElement`.

### How the coordinate math works
- Render endpoint returns PNG at `dpi=144`; `PyMuPDF page.rect` is in PDF native units (points, 72/inch).
- Panel fetches `/pages/{n}` to get native `width`/`height`.
- For each bbox `{x0, y0, x1, y1}` in native units: `left = x0 * (renderedWidth / nativeWidth)`, analogous for y. `ResizeObserver` on `.pdf-render-inner` keeps `renderedSize` current on viewport changes. No DPI assumption in the hot path.
- Fallback when `width/height` is missing (old `.pages.json` persisted before this change): derives native size from `img.naturalWidth * 72/144`. Math still works since render DPI is fixed.

### Migration for existing uploads
- Existing `.pages.json` / `.chunks.json` load fine (all new fields have defaults). They just carry zero-size `width/height` and empty `bbox_regions`, so the panel shows the status hint "当前文档缺少 bbox（旧版解析），请重新上传以启用高亮" instead of overlays.
- New uploads go through the PyMuPDF parser and get full bbox metadata automatically.
- No DB/schema migration: everything is file-based JSON under `data/parsed/`.

### Verification
- Backend: 54/54 pytest green. Roundtrip test on a real CJK academic PDF from `data/uploads/` — 35 chunks, each with populated `bbox_regions`, native page 595×842, block count 18 on page 1. Render endpoint produces ~320KB PNG per A4 page at 144 dpi.
- Frontend: 7/7 smoke tests green, `tsc --noEmit` clean.
- Not yet verified: live visual inspection in dev server. The golden path (upload PDF → ask → click 打开定位 → see yellow rectangle on the page text) was not run interactively in this session.

### Known trade-offs
- **Bbox granularity = PyMuPDF blocks.** A block is typically a paragraph. So the highlight covers the whole paragraph that contains the evidence, not just the sentence. For a demo this is usually fine (still unambiguous), and for dense CJK it's actually more robust than sentence-level. If the judges want sentence-level precision, the path is `page.get_text("dict")` → span-level bboxes and merging spans that share a snippet match — extra ~1 day of work.
- **One render endpoint hit per page switch.** No cache. Acceptable at 200–400KB/page; if demo machine is slow, add `Cache-Control: private, max-age=3600` on the render response.

### Files touched
- `backend/requirements.txt`
- `backend/app/schemas/document.py`
- `backend/app/schemas/task.py`
- `backend/app/services/document_parser.py`
- `backend/app/services/chunk_service.py`
- `backend/app/services/task_service.py`
- `backend/app/services/file_service.py`
- `backend/app/api/routes.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/components/ResultPanel.tsx`
- `frontend/src/components/PdfPreviewPanel.tsx`
- `frontend/src/styles.css`
- `frontend/src/App.smoke.test.tsx`

### Next round suggestions
- Run dev server + smoke the end-to-end flow visually on one PDF; screenshot for TASK_BOARD.
- If highlight rectangles look too-paragraph-big on pedagogical demos, upgrade to span-level bbox via `get_text("dict")`.

---

## 2026-04-17 — line-level bbox 精细化

### 背景
上一轮 (ead90ac) 发布的 PDF 高亮基于 PyMuPDF **block 级** bbox，而 block 通常是整段。chunk 合并多个 block 后，overlay 覆盖了整节（用户截图显示 5.1 节被一整块橙色覆盖）。用户反馈："高量做的很不好"。

### 方案
换到 **line 级**，并在返回 citation 时用 snippet 原句对 line 序列做子串匹配，只高亮匹配到的那几行。粒度从"段"缩到"句/行"。

### 改动
- `document.py`: 新增 `ParsedLine`; `ParsedPage.lines: list[ParsedLine] = []`（默认空，保持旧 JSON 兼容）
- `document_parser.py`: 新 `_extract_lines(page)` 用 `page.get_text("dict")` 拆 blocks→lines→spans，拿每行 bbox
- `bbox_matcher.py`（新）: `match_snippet_to_line_bboxes(page_number, page_lines, snippet)`。思路：
  - 把所有行文本拼起来做一个"源串"，记下每个 non-whitespace 字符到原 index 的映射
  - snippet 也压缩掉空白再做子串查找；找到范围后反查覆盖到哪些行
  - 找不到就按标点切成 fragment，挑最长的再试一轮
- `task_service.py`:
  - `_build_pages_index`：开头调一次，拿 `{page_number: [ParsedLine]}`
  - `_attach_line_bboxes(citations, pages_index, *, quote_by_chunk=None)`：就地替换 `citation.bbox_regions`
  - ask 路径：优先用 `evidence_quotes`（模型抽取的原文）匹配，fallback snippet
  - 三个 TaskResult 构造点（refusal 空跳过、cached、fresh）都接上

### 策略选择
找不到匹配时 **清空** bbox_regions 而不是 fallback 到 block 级。理由：用户已明确表态"大片橙色"是负面观感，宁可没高亮也不要错高亮。如果后续反馈"经常没高亮"，再考虑 fallback。

### 验证
- 后端 54/54 pytest 绿
- 真 PDF roundtrip：7 页文档重新解析，7/7 页都有 lines；中间一页 56 lines vs 26 blocks（2× 粒度提升）。单行/多行/部分匹配都精确命中
- 前端 7/7 vitest 绿，`tsc --noEmit` 净
- **未做**：live 视觉验收。旧 `.pages.json` 没有 lines，要重新上传 PDF 才能看到效果

### Migration
- 旧 JSON 有默认 `lines: []`，load 不报错，但 `_attach_line_bboxes` 会给空 bbox_regions，结果就是"没高亮"
- 用户重新上传一次就自动走新 parser

### Commit
`f1feaf1 feat(pdf): line-level bbox matching for precise highlighting`

### 下一轮建议
- 跑 dev server，重新上传用户截图那个 PDF，再问一次同样的问题，看高亮是否缩到一两句
- 如果"没高亮"的 citation 比例偏高，放开 fallback：snippet 匹配失败时保留原 chunk block bbox

---

## 2026-04-18 — Wuwen Xinqiong real minimal path validated

### 背景
当前优化主线已经切到比赛/评审准备，主链路目标是 `ask -> citation -> PDF -> refusal`。本轮继续按照 `agent_handoff/COMPETITION_PLAN_V2.md` 和 `agent_handoff/CURRENT_STATUS_20260418.md` 推进，验证当前新的 `.env` 是否已经能在项目内真正跑通无问芯穹闭环。

### 关键发现
- 当前活动 `.env` 确实是新的 `Wuwen Xinqiong` 配置；旧 replay 报告里出现的旧 provider 只能当历史记录，不代表当前运行态。
- 最初一次“中文问题检索不到”的现象不是产品 bug，而是 PowerShell 把 inline Python 的中文字面量转成了 `?`，导致调试脚本自己把 query 发坏了。
- 在允许真实出网后，项目内最小闭环已经跑通。

### 本轮验证
- 样例文档：`evidence/samples/chinese_llm_spatial_eval.pdf`
- 路径：`login -> upload -> ask -> citation -> GET cited page -> GET cited page render`
- 结果：
  - `ask` 成功
  - 模型：`qwen3-235b-a22b-instruct-2507`
  - 检索状态：`matched`
  - 引用数：`2`
  - 典型延迟：约 `6686 ms`
  - cited page 接口：通过
  - cited render 接口：通过，返回 `image/png`
- 同一问题随后命中缓存，`cache_hit=true`，说明当前缓存键路径也正常工作。

### 观察到的引用情况
- `used_chunk_ids` 命中了第 `2`、`3` 页相关 chunk
- `evidence_quotes` 抽到了“本研究拟探究以下问题……”与 “本研究基于第四届中文空间语义理解评测任务（SpaCE2024）……” 两段
- bbox/page 回链正常，可继续作为主演示链的一部分

### 拒答观察
- 半相关问题（带有文档内实体，例如“作者”）可能会命中检索并得到回答，所以不适合作为最终 refusal demo prompt
- 真正纯离题的问题 `木星有几颗卫星？` 被正确拒答：
  - `outcome=refused`
  - `retrieval_status=no_match`
  - 延迟约 `38 ms`

### 当前结论
- 无问芯穹接入本身不再是 blocker
- 项目已经从“接通 provider”进入“锁 gold sample + 比较 QA 模型 + 刷新真实证据”的阶段
- 当前最需要的是：
  - 锁 `2 answerable + 1 refusal` 候选问题
  - 用同一路径比较 `qwen3-235b-a22b-instruct-2507` 与 `qwen3-32b`
  - 刷新真实截图和 replay/evidence

---

## 2026-04-18 — Gold-sample candidate locked and QA models compared

### 背景
上一轮已经确认当前新的 `.env` 下，`Wuwen Xinqiong` 项目内最小闭环是通的。本轮继续沿着 `COMPETITION_PLAN_V2` 推进，把“候选 gold sample + 题集 + QA 模型决策”固化下来，而不是再做泛化功能。

### 新增资产
- 候选题集清单：
  - `evidence/materials/GOLD_SAMPLE_CANDIDATE_20260418.json`
- 可复跑比较脚本：
  - `scripts/compare_qa_models.py`
- 最新对比报告：
  - `evidence/reports/gold_sample_qa_compare_latest.md`
  - `evidence/reports/gold_sample_qa_compare_latest.json`

### 锁定的 gold-sample candidate
- 文档：
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
- 候选问题：
  - answerable 1：`这篇论文主要研究了什么问题？`
  - answerable 2：`作者最终的方法排名和总体准确率分别是多少？`
  - refusal：`木星有几颗卫星？`

### 对比方式
- 使用当前真实 `Wuwen Xinqiong` 运行时
- 不走旧 replay 脚本，而是按当前 session/cookie/document token 边界直接通过服务层跑真实 `ask`
- 每个模型都验证：
  - ask 是否成功
  - citations 是否返回
  - cited page 是否能读取
  - cited page render 是否能返回 PNG
  - refusal 是否真正 `refused`

### 对比结果
- `qwen3-235b-a22b-instruct-2507`
  - `3 / 3` 通过
  - 平均延迟约 `4896 ms`
  - 两个 answerable 都返回了更丰富的 citations / evidence quotes
- `qwen3-32b`
  - `3 / 3` 通过
  - 平均延迟约 `4396 ms`
  - 也能通过全部候选题，但通常返回更少的 citations / evidence quotes

### 当前决策
- 保持 `qwen3-235b-a22b-instruct-2507` 作为当前默认 `MODEL_QA`
- 原因不是“绝对更快”，而是：
  - 当前差距只有约 `500 ms`
  - 但 `235b` 在 broad ask 上给出的 grounding 更丰满
  - 比赛/demo 叙事里，“证据感更强”比这点延迟更值钱
- `qwen3-32b` 已经完成同题集验证，可作为后续延迟受限时的 fallback

### 后续建议
- 现在更值得做的是刷新真实证据与截图，而不是继续横向加功能
- 如果后面部署环境出现更紧的延迟压力，再用同一个脚本重跑一次，确认是否要把默认 QA 切到 `qwen3-32b`

---

## 2026-04-18 — Replay workflow updated to current auth boundary

### 背景
虽然 `compare_qa_models.py` 已经能验证锁定候选题集，但 repo 里的旧 `replay_sample_set.py` 仍然停留在无 session / 无 document token 的旧执行姿态。继续沿用它会让“latest replay”工具链和现在真实运行态脱节。

### 本轮改动
- `scripts/replay_sample_set.py`
  - 新增 `AuthService`
  - 内部自动创建 controlled-alpha session
  - 上传时写入 `owner_session_id`
  - 执行任务时传入：
    - `session_id`
    - `document_access_token`
    - `response_detail_level`
  - 新增对两类 manifest 的兼容：
    - 旧版 list + `tasks`
    - 新版 dict + `prompts`（gold-sample candidate ask-only）
  - 新增 `--invite-code`
- `scripts/run_real_replay.ps1`
  - 新增 `-Manifest`
  - 新增 `-NamePrefix`
  - 因此现在可以一键刷新 broad sample set，也可以一键刷新 locked gold-sample candidate
- `evidence/materials/REAL_REPLAY_GUIDE.md`
  - 已同步更新说明

### 验证
- `py_compile` 通过
- mock 下用 `GOLD_SAMPLE_CANDIDATE_20260418.json` 跑通
- 真实环境下用：
  - `powershell -ExecutionPolicy Bypass -File .\scripts\run_real_replay.ps1 -Manifest evidence\materials\GOLD_SAMPLE_CANDIDATE_20260418.json -NamePrefix gold_sample_replay_real`
  - 成功刷新：
    - `evidence/reports/gold_sample_replay_real_latest.md`
    - `evidence/reports/gold_sample_replay_real_summary_latest.md`
    - `evidence/reports/latest_log_summary.md`

### 结果
- 当前主模型 `qwen3-235b-a22b-instruct-2507` 下：
  - answerable 1：通过，有 citations
  - answerable 2：通过，有 citations
  - refusal：通过，`retrieval_status=no_match`
- 这意味着：
  - compare 脚本可用于“模型决策”
  - replay 脚本可用于“权威 latest evidence 输出”
  - 两条链现在都已经对齐到当前真实运行边界

---

## 2026-04-18 – Gold-sample materials aligned

### 背景
在锁定 gold-sample candidate、完成 QA 模型比较、修好 replay 工具链之后，下一步不该继续泛化功能，而是把这组固定题和固定文档沉到“可直接照着演示/截图”的材料层。

### 本轮改动
- 新增：
  - `evidence/materials/GOLD_SAMPLE_RUNBOOK.md`
- 更新：
  - `evidence/materials/DEMO_SCRIPT_3MIN.md`
  - `evidence/materials/QA_BRIEF.md`
  - `evidence/materials/MATERIALS_INDEX.md`
  - `evidence/materials/REAL_EVIDENCE_REFRESH_CHECKLIST.md`

### 作用
- 演示脚本不再停留在“问一个典型问题”，而是明确绑定到当前锁定题集
- QA 提纲不再泛泛而谈“下一步做真实复跑”，而是转成“用 gold-sample candidate 刷新真实证据并产出比赛材料”
- 证据刷新清单不再优先 broad sample set，而是优先当前锁定候选题
- 后续无论是 Codex、Claude 还是人工操作，都能直接按 `GOLD_SAMPLE_RUNBOOK.md` 执行，不必现场重选题

### 当前更清晰的顺序
1. 按 `GOLD_SAMPLE_RUNBOOK.md` 跑现场演示
2. 刷新截图
3. 用已有 compare/replay 报告做 paper/PPT/video/poster 的事实底稿

---

## 2026-04-18 / Codex

- Summary:
  - Aligned runtime/deploy docs to the current `Wuwen Xinqiong` baseline instead of the older Ark wording
  - Promoted the locked gold-sample candidate to the default judging/demo replay path across replay/material docs
  - Updated shared handoff files so the next operator sees screenshot/material production as the primary next step
- Files touched:
  - `.env.example`
  - `README.md`
  - `WORKLOG.md`
  - `render.yaml`
  - `docs/DEPLOY_RENDER.md`
  - `evidence/materials/ARCHITECTURE.md`
  - `evidence/materials/SAMPLE_SET.md`
  - `evidence/materials/PROJECT_ONE_PAGER.md`
  - `evidence/materials/REAL_REPLAY_GUIDE.md`
  - `evidence/materials/MATERIALS_INDEX.md`
  - `agent_handoff/CURRENT_STATUS_20260418.md`
  - `agent_handoff/TASK_BOARD.md`
  - `agent_handoff/PROJECT_HANDOFF.md`
  - `agent_handoff/SESSION_LOG.md`
- Verification:
  - doc-only alignment round; no new runtime behavior introduced
  - checked that the current authoritative evidence artifacts remain:
    - `evidence/reports/gold_sample_qa_compare_latest.md`
    - `evidence/reports/gold_sample_replay_real_latest.md`
    - `evidence/reports/gold_sample_replay_real_summary_latest.md`
- Open risks:
  - broader sample-set replay artifacts still exist and may confuse future operators if they skip the updated handoff/material docs
  - fresh screenshot evidence is still the main remaining judging/demo gap
- Recommended next step:
  - capture the fresh gold-sample screenshots and fold them into PPT / video / poster materials

---

## 2026-04-18 / Codex (gold-sample screenshot automation + refresh)

- Summary:
  - Added an automated browser screenshot script for the locked gold-sample path
  - Refreshed the four core judging/demo screenshots under the current real `Wuwen Xinqiong` runtime
  - Updated evidence docs and shared handoff files so screenshot refresh is no longer tracked as the main open gap
- Files touched:
  - `scripts/capture_gold_sample_screenshots.js`
  - `evidence/README.md`
  - `evidence/experiments/20260418_gold_sample_validation.md`
  - `evidence/materials/REAL_EVIDENCE_REFRESH_CHECKLIST.md`
  - `agent_handoff/CURRENT_STATUS_20260418.md`
  - `agent_handoff/TASK_BOARD.md`
  - `agent_handoff/PROJECT_HANDOFF.md`
  - `agent_handoff/SESSION_LOG.md`
  - `evidence/screenshots/20260418_gold_ask_research_focus.png`
  - `evidence/screenshots/20260418_gold_pdf_render.png`
  - `evidence/screenshots/20260418_gold_ask_rank_accuracy.png`
  - `evidence/screenshots/20260418_gold_refusal.png`
- Verification:
  - real run succeeded via `node scripts/capture_gold_sample_screenshots.js`
  - created screenshots:
    - `evidence/screenshots/20260418_gold_ask_research_focus.png`
    - `evidence/screenshots/20260418_gold_pdf_render.png`
    - `evidence/screenshots/20260418_gold_ask_rank_accuracy.png`
    - `evidence/screenshots/20260418_gold_refusal.png`
- Open risks:
  - the script currently covers the four core gold-sample screenshots only, not the optional stats-panel or backend API-docs captures
  - the script depends on `frontend/dist` being available locally
- Recommended next step:
  - use the refreshed screenshots plus the existing compare/replay reports to build the final PPT / video / poster asset pack

---

## 2026-04-18 / Codex (competition asset-pack consolidation)

- Summary:
  - Added a dedicated competition asset-pack doc so PPT / video / poster assembly now follows one locked source instead of ad hoc file picking
  - Rewrote the submission-prep guide onto the current gold-sample-primary story
  - Updated handoff/task docs so the next operator moves from “collect assets” to “assemble final deliverables”
- Files touched:
  - `evidence/materials/COMPETITION_ASSET_PACK.md`
  - `evidence/materials/SUBMISSION_PREP_GUIDE.md`
  - `evidence/materials/MATERIALS_INDEX.md`
  - `agent_handoff/CURRENT_STATUS_20260418.md`
  - `agent_handoff/TASK_BOARD.md`
  - `agent_handoff/PROJECT_HANDOFF.md`
  - `agent_handoff/SESSION_LOG.md`
- Verification:
  - doc-only material-consolidation round
  - checked the asset pack points only to current locked assets:
    - `GOLD_SAMPLE_CANDIDATE_20260418.json`
    - `gold_sample_qa_compare_latest.md`
    - `gold_sample_replay_real_summary_latest.md`
    - the four `20260418_gold_*.png` screenshots
- Open risks:
  - final PPT / video / poster files themselves are still not authored in-repo
  - optional stats-panel and backend API-docs screenshots remain uncaptured
- Recommended next step:
  - turn `COMPETITION_ASSET_PACK.md` into the actual submission deliverables

---

## 2026-04-18 / Codex (full screenshot pack completed)

- Summary:
  - Extended the browser screenshot script to also capture the stats panel and backend API-docs page
  - Refreshed the final six-file screenshot pack under the locked `20260418_*` naming
  - Updated evidence/handoff docs so screenshot refresh is now fully closed, not partially complete
- Files touched:
  - `scripts/capture_gold_sample_screenshots.js`
  - `evidence/README.md`
  - `evidence/experiments/20260418_gold_sample_validation.md`
  - `evidence/materials/REAL_EVIDENCE_REFRESH_CHECKLIST.md`
  - `evidence/materials/COMPETITION_ASSET_PACK.md`
  - `agent_handoff/CURRENT_STATUS_20260418.md`
  - `agent_handoff/TASK_BOARD.md`
  - `agent_handoff/PROJECT_HANDOFF.md`
  - `agent_handoff/SESSION_LOG.md`
  - `evidence/screenshots/20260418_stats_panel.png`
  - `evidence/screenshots/20260418_api_docs.png`
- Verification:
  - real run succeeded via:
    - `$env:SCREENSHOT_DATE_OVERRIDE='20260418'; node scripts/capture_gold_sample_screenshots.js`
  - final screenshot set now includes:
    - `20260418_gold_ask_research_focus.png`
    - `20260418_gold_pdf_render.png`
    - `20260418_gold_ask_rank_accuracy.png`
    - `20260418_gold_refusal.png`
    - `20260418_stats_panel.png`
    - `20260418_api_docs.png`
- Open risks:
  - only the raw screenshot assets are complete; the actual PPT / video / poster files still need assembly
- Recommended next step:
  - use `COMPETITION_ASSET_PACK.md` to assemble the final submission deliverables

---

## 2026-04-18 / Codex (deliverable drafting pack added)

- Summary:
  - Added ready-to-use PPT, video, and poster drafting docs bound to the locked gold-sample story
  - Added a PowerShell export script so the full competition material set can be copied into a timestamped handoff bundle
  - Updated shared status docs so “next work” now means final asset production rather than ad hoc material picking
- Files touched:
  - `evidence/materials/PPT_DECK_6SLIDES.md`
  - `evidence/materials/VIDEO_SHOTLIST_2MIN.md`
  - `evidence/materials/POSTER_COPY.md`
  - `scripts/export_competition_asset_pack.ps1`
  - `.gitignore`
  - `evidence/materials/COMPETITION_ASSET_PACK.md`
  - `evidence/materials/MATERIALS_INDEX.md`
  - `evidence/materials/SUBMISSION_PREP_GUIDE.md`
  - `evidence/README.md`
  - `evidence/experiments/20260418_gold_sample_validation.md`
  - `WORKLOG.md`
  - `agent_handoff/CURRENT_STATUS_20260418.md`
  - `agent_handoff/PROJECT_HANDOFF.md`
  - `agent_handoff/TASK_BOARD.md`
  - `agent_handoff/SESSION_LOG.md`
- Verification:
  - deliverable docs all point to the locked gold-sample candidate and current authoritative screenshots/reports
  - export script is intended to package:
    - `PROJECT_ONE_PAGER.md`
    - `DEMO_SCRIPT_3MIN.md`
    - `COMPETITION_ASSET_PACK.md`
    - the three new drafting docs
    - current authoritative reports
    - the locked screenshot set
    - the locked sample PDF
- Open risks:
  - final `.pptx`, edited video, and laid-out poster files still need to be produced outside markdown
  - staging/demo environment should still be smoke-checked before formal judging
- Recommended next step:
  - generate one export bundle and use it as the single source for final slide/video/poster file production

---

## 2026-04-19 / Codex (printable deck/poster prototypes added)

- Summary:
  - Added a repo-native six-slide HTML deck prototype and poster HTML prototype
  - Both prototypes are aligned to the locked gold-sample wording and current authoritative screenshots
  - Updated materials/handoff docs so later operators treat these HTML files as the default visual baseline for final production
- Files touched:
  - `deliverables/competition_kit/README.md`
  - `deliverables/competition_kit/deck.html`
  - `deliverables/competition_kit/poster.html`
  - `deliverables/competition_kit/styles.css`
  - `evidence/materials/MATERIALS_INDEX.md`
  - `evidence/materials/SUBMISSION_PREP_GUIDE.md`
  - `WORKLOG.md`
  - `agent_handoff/CURRENT_STATUS_20260418.md`
  - `agent_handoff/PROJECT_HANDOFF.md`
  - `agent_handoff/TASK_BOARD.md`
  - `agent_handoff/SESSION_LOG.md`
- Verification:
  - HTML references point to the locked `20260418_*` screenshot set
  - the prototypes only use the current locked story:
    - `chinese_llm_spatial_eval.pdf`
    - `2 answerable + 1 refusal`
    - `qwen3-235b-a22b-instruct-2507` primary
    - `qwen3-32b` fallback
- Open risks:
  - browser-side print/export to final PDF still needs one operator pass
  - final video file still needs timeline editing outside repo markdown/html
- Recommended next step:
  - print `deck.html` and `poster.html` to PDF, then decide whether any last-mile visual polish is still needed

---

## 2026-04-19 / Codex (PDF export scripted)

- Summary:
  - Added `scripts/export_competition_pdfs.js` to export the deck/poster PDFs through CDP instead of relying on browser CLI flags
  - Updated materials and handoff docs so PDF export is now a named repo step
  - The visual-material path is now: markdown copy -> HTML prototype -> scripted PDF export
- Files touched:
  - `scripts/export_competition_pdfs.js`
  - `deliverables/competition_kit/README.md`
  - `evidence/materials/MATERIALS_INDEX.md`
  - `evidence/materials/SUBMISSION_PREP_GUIDE.md`
  - `WORKLOG.md`
  - `agent_handoff/CURRENT_STATUS_20260418.md`
  - `agent_handoff/PROJECT_HANDOFF.md`
  - `agent_handoff/TASK_BOARD.md`
  - `agent_handoff/SESSION_LOG.md`
- Verification:
  - script targets:
    - `deliverables/competition_kit/deck.html -> deck.pdf`
    - `deliverables/competition_kit/poster.html -> poster.pdf`
  - script uses the same local browser-discovery approach already proven by screenshot automation
- Open risks:
  - final exported PDF visuals still need one visual inspection pass
  - video output itself still needs editing outside repo
- Recommended next step:
  - inspect the generated PDFs and only do last-mile cosmetic polish if necessary

---

## 2026-04-19 / Codex (PDF baselines exported)

- Summary:
  - Ran `node scripts/export_competition_pdfs.js` with the necessary browser permission and exported the current deck/poster PDF baselines
  - Shared status docs now treat the PDFs as existing outputs, not only as potential exports
- Files touched:
  - `deliverables/competition_kit/README.md`
  - `deliverables/competition_kit/deck.pdf`
  - `deliverables/competition_kit/poster.pdf`
  - `WORKLOG.md`
  - `agent_handoff/CURRENT_STATUS_20260418.md`
  - `agent_handoff/PROJECT_HANDOFF.md`
  - `agent_handoff/TASK_BOARD.md`
  - `agent_handoff/SESSION_LOG.md`
- Verification:
  - script completed successfully:
    - `Created deliverables\competition_kit\deck.pdf`
    - `Created deliverables\competition_kit\poster.pdf`
- Open risks:
  - PDFs still need one eyeball pass for layout polish
  - final video output still needs timeline editing outside repo
- Recommended next step:
  - use the exported PDFs as the current baseline deliverables and only iterate if visual polish is still required

---

## 2026-04-19 / Codex (asset bundle upgraded to carry deliverables)

- Summary:
  - Updated `scripts/export_competition_asset_pack.ps1` so the exported bundle now includes the HTML/PDF deliverables and the PDF re-export script
  - Material indexes and handoff docs now point to the full bundle as the default external handoff artifact
- Files touched:
  - `scripts/export_competition_asset_pack.ps1`
  - `evidence/materials/COMPETITION_ASSET_PACK.md`
  - `evidence/materials/MATERIALS_INDEX.md`
  - `evidence/materials/SUBMISSION_PREP_GUIDE.md`
  - `WORKLOG.md`
  - `agent_handoff/CURRENT_STATUS_20260418.md`
  - `agent_handoff/PROJECT_HANDOFF.md`
  - `agent_handoff/TASK_BOARD.md`
  - `agent_handoff/SESSION_LOG.md`
- Verification:
  - required export list now also includes:
    - `deliverables/competition_kit/deck.html`
    - `deliverables/competition_kit/poster.html`
    - `deliverables/competition_kit/deck.pdf`
    - `deliverables/competition_kit/poster.pdf`
    - `scripts/export_competition_pdfs.js`
- Open risks:
  - full bundle should still be regenerated once after any future visual polish
- Recommended next step:
  - run the upgraded asset-pack export once and use that directory as the canonical handoff bundle

---

## 2026-04-19 / Codex (video subtitle baseline added)

- Summary:
  - Added `deliverables/competition_kit/video_subtitles.srt` as a timed subtitle / narration baseline for the 2-minute demo video
  - Updated the asset bundle so this file ships with the rest of the competition deliverables
- Files touched:
  - `deliverables/competition_kit/video_subtitles.srt`
  - `deliverables/competition_kit/README.md`
  - `scripts/export_competition_asset_pack.ps1`
  - `evidence/materials/COMPETITION_ASSET_PACK.md`
  - `evidence/materials/MATERIALS_INDEX.md`
  - `evidence/materials/SUBMISSION_PREP_GUIDE.md`
  - `WORKLOG.md`
  - `agent_handoff/CURRENT_STATUS_20260418.md`
  - `agent_handoff/PROJECT_HANDOFF.md`
  - `agent_handoff/TASK_BOARD.md`
  - `agent_handoff/SESSION_LOG.md`
- Verification:
  - subtitle timing matches the current `VIDEO_SHOTLIST_2MIN.md` section boundaries
  - export bundle required-file list now includes `deliverables/competition_kit/video_subtitles.srt`
- Open risks:
  - final recorded video still needs actual editing/rendering outside repo
- Recommended next step:
  - keep the current subtitle file as the canonical baseline and adjust only if the final cut changes shot timing

---

## 2026-04-19 / Codex (external AI review bundle prepared)

- Summary:
  - Created a curated external-review bundle for third-party AI review of the current competition state
  - Added a dedicated `REVIEW_PROMPT.md` that asks the reviewer to judge strategy, evidence, materials, technical risks, and gate completion
  - Bundled goal/background docs, key evidence, current deliverables, and core code files without including secrets
- Local artifact paths:
  - directory: `review_bundle_stage_20260419_003447/`
  - zip: `review_bundle_20260419_003447_competition_ai_review.zip`
- Bundle highlights:
  - includes:
    - `agent_handoff/COMPETITION_PLAN_V2.md`
    - `agent_handoff/CURRENT_STATUS_20260418.md`
    - `evidence/materials/COMPETITION_ASSET_PACK.md`
    - `evidence/reports/gold_sample_replay_real_summary_latest.md`
    - current screenshots / PDFs / subtitle baseline
    - selected backend/frontend/script files for code-level review
  - excludes:
    - `.env`
    - unrelated external-strategy files
    - cache/temp/runtime noise
- Verification:
  - copied `52` curated project files into the bundle
  - zip created successfully:
    - `review_bundle_20260419_003447_competition_ai_review.zip`
- Open risks:
  - this is a local review artifact and is not intended as a canonical long-term repo deliverable by default
- Recommended next step:
  - hand the zip plus `REVIEW_PROMPT.md` to external AI reviewers and compare their gate/completion judgments against the current internal plan

---

## 2026-04-19 / Codex (review-driven hardening + refreshed evidence pack)

- Summary:
  - Converted the highest-value external-review findings into concrete code and material fixes
  - Closed the main screenshot/evidence inconsistency in the current judging path
  - Refreshed the gold-sample screenshot pack under the current `.env` and regenerated deliverables/export bundle
- Files touched:
  - `frontend/src/App.tsx`
  - `frontend/src/components/ResultPanel.tsx`
  - `backend/app/services/model_client.py`
  - `backend/app/services/task_service.py`
  - `scripts/capture_gold_sample_screenshots.js`
  - `scripts/export_competition_asset_pack.ps1`
  - `deliverables/competition_kit/deck.html`
  - `deliverables/competition_kit/poster.html`
  - `deliverables/competition_kit/deck.pdf`
  - `deliverables/competition_kit/poster.pdf`
  - `evidence/materials/COMPETITION_ASSET_PACK.md`
  - `evidence/materials/PPT_DECK_6SLIDES.md`
  - `evidence/materials/POSTER_COPY.md`
  - `evidence/materials/REAL_EVIDENCE_REFRESH_CHECKLIST.md`
  - `evidence/materials/SUBMISSION_PREP_GUIDE.md`
  - `evidence/materials/VIDEO_SHOTLIST_2MIN.md`
  - `WORKLOG.md`
  - `agent_handoff/CURRENT_STATUS_20260418.md`
  - `agent_handoff/PROJECT_HANDOFF.md`
  - `agent_handoff/TASK_BOARD.md`
  - `agent_handoff/SESSION_LOG.md`
- Verification:
  - `npm run build`
  - `npm test -- --run` -> `7 passed`
  - `.venv\Scripts\python.exe -m pytest` -> `54 passed`
  - `node scripts\capture_gold_sample_screenshots.js` refreshed `20260419_*` screenshots successfully
  - refreshed sidecars confirm:
    - `20260419_gold_ask_research_focus.json` -> `declared`
    - `20260419_gold_ask_rank_accuracy.json` -> `declared` on retry attempt `2`
    - `20260419_gold_refusal.json` -> `none`
  - `node scripts\export_competition_pdfs.js` refreshed printable PDF baselines
  - `powershell -ExecutionPolicy Bypass -File .\scripts\export_competition_asset_pack.ps1` produced:
    - `evidence/exports/competition_asset_pack_20260419_012336/`
- Open risks:
  - `G3` still lacks second-operator / 3-run / <=3-minute evidence
  - final deck/poster/video still need human polish outside repo
- Recommended next step:
  - perform the formal `G3` rehearsal and record it as the next gate-closing artifact

---

## 2026-04-19 / Codex (G3 rehearsal prep hardened)

- Summary:
  - Added pre-demo warmup, fallback rules, and explicit `G3` recording requirements to `GOLD_SAMPLE_RUNBOOK.md`
  - Added a reusable rehearsal log template for the second operator
- Files touched:
  - `evidence/materials/GOLD_SAMPLE_RUNBOOK.md`
  - `evidence/experiments/20260419_g3_rehearsal_template.md`
- Practical meaning:
  - the next operator no longer needs to invent a `G3` logging format
  - fallback behavior is now written down before the rehearsal rather than improvised during it
