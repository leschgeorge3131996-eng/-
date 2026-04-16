# Agent Handoff Folder

This folder is the shared context area for both Codex and Claude Code.

Goal:

- keep one canonical handoff package inside the repo
- make future model switches low-friction
- avoid losing context in chat history only

## Read Order

At the start of a new session, read files in this order:

1. `agent_handoff/PROJECT_HANDOFF.md`
2. `agent_handoff/TASK_BOARD.md`
3. `agent_handoff/SESSION_LOG.md`
4. `WORKLOG.md`
5. `README.md`

Then run:

```powershell
git status --short
```

## Update Rules

After each meaningful work session:

1. Append one entry to `SESSION_LOG.md`
2. Update `TASK_BOARD.md` if priorities changed
3. Update `PROJECT_HANDOFF.md` only if architecture, runtime posture, or demo strategy changed

## What To Put Here

Put only durable shared context here:

- current project state
- recent architectural changes
- verified commands and test status
- known risks
- next-step priorities
- session summaries

Do not put secrets here.

Do not copy `.env` or API keys here.

## Current Shared Convention

- Treat login / invite-code / cookie session as a controlled-alpha boundary, not a product highlight
- Treat evidence-backed `ask` as the main product differentiator
- Prefer demo and judging readiness over expanding product scope
- Avoid adding new task types unless explicitly requested by the user

## Disposable Artifacts

Generated review bundles such as `review_bundle_stage_*` are disposable.
They are useful for external review, but they are not the canonical shared context.
