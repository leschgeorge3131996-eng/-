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
