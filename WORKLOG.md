# WORKLOG

## Project

- Name: `研答通`
- Goal: build a document assistant MVP with upload, cloud-model processing, result display, and local logs.
- Principle: first make the smallest runnable loop, then enhance step by step.

## Current Status

- Phase: `P1 / Demo-ready prototype`
- Status: `running end-to-end with retrieval, citations, stats, sample replay tooling, and competition materials`
- Verified on: `2026-04-15`

### Completed

- React + TypeScript + Vite frontend created
- FastAPI backend created
- Upload support for `TXT / Markdown / PDF`
- Parsed text saved to `data/parsed/`
- Raw uploads saved to `data/uploads/`
- Tasks implemented:
  - `summary`
  - `ask`
  - `outline`
- Unified API response shape implemented
- Model client isolated in `backend/app/services/model_client.py`
- Local JSONL logs implemented in `data/logs/call_logs.jsonl`
- Swagger docs available at `http://localhost:8000/docs`
- Real cloud integration switched from mock to `Volcengine Ark`
- Local result cache added for repeated requests
- Frontend staged loading states added
- Duplicate submit prevention added
- Friendlier burst-limit error handling added
- Recent document reuse added in frontend
- Recent result history added in frontend
- Log summary API added
- Log summary export script added
- Evidence directory and experiment template added
- Document fingerprint added to upload metadata and task results
- Clearer truncation feedback added to task results
- API integration tests added for upload, tasks, and log summary
- Frontend stats panel added
- Demo mode added with sample document and sample prompts
- Parsed document structure now saved for TXT/MD/PDF
- PDF page-aware structure is available as stored parsed output
- Chunked document structure now saved to parsed outputs
- Ask task now uses lightweight retrieval over chunks
- Ask task now returns structured citations with page numbers and snippets
- Context planner added for task-specific context selection
- Summary and outline now use chunk coverage context instead of plain whole-text truncation
- Ask retrieval now rejects low-relevance questions instead of fabricating evidence
- Summary and outline now also expose source chunk citations
- Log summary now tracks retrieval status and citation counts
- Task outcome semantics added: answered / refused / error
- Frontend now distinguishes citations vs source chunks by task type
- Retrieval now includes query normalization, stopword filtering, title bonus, and stable chunk ids
- Competition materials have been refined into reusable review/demo docs
- Minimal model tier routing is implemented and test-covered
- Fixed sample set replay script is available
- Sample replay report can now be exported with route and evidence stats
- One-click real replay script is available
- English paper end-to-end validation has been recorded in evidence
- Chinese academic PDF sample has been added to sample set
- Frontend result panel now exposes route tier and route reason
- Log summary now normalizes legacy outcome values and aggregates route tiers
- Evidence refresh checklist and submission prep guide have been added
- Real fixed-sample replay has been completed once with the real cloud model
- Response detail control now supports `concise / balanced / detailed` across frontend, API, prompt routing, cache, and logs
- Ask grounding now includes model-declared `used_chunk_ids` and `evidence_quotes`
- Replay reports now aggregate response detail levels and grounding counts

### Verified Results

- Frontend upload works
- `summary` works with real model
- `ask` works with real model
- `outline` works with real model
- API docs page works
- Call logs are written locally
- Backend tests pass: `27 passed`
- Log summary exported to `evidence/reports/latest_log_summary.md`
- Sample replay report exported to `evidence/reports/sample_replay_latest.md`
- Real replay report exported to `evidence/reports/sample_replay_real_latest.md`
- Real replay summary exported to `evidence/reports/sample_replay_real_summary_latest.md`
- English paper validation recorded in `evidence/experiments/20260415_attention_is_all_you_need_validation.md`

## Current Runtime Configuration

- Provider: `volcengine_ark`
- Base URL: `https://ark.cn-beijing.volces.com/api/v3`
- Current endpoint id:
  - `MODEL_QA=ep-m-20260401130050-qn8nk`
  - `MODEL_SUMMARY=ep-m-20260401130050-qn8nk`
  - `MODEL_OUTLINE=ep-m-20260401130050-qn8nk`

Notes:

- Real API key is stored only in `.env`
- Do not copy secrets into source files or commit logs with secrets

## Key Evidence Collected

- Frontend success screenshot exists
- Log screenshot exists
- Swagger/API screenshot exists
- Sample replay report exists
- Real sample replay report exists
- One-page project summary exists
- Demo script exists
- Sample set exists
- Architecture note exists
- QA brief exists
- Real call logs contain:
  - `model_name`
  - `success`
  - `latency_ms`
  - `token_in / token_out / token_total`

## Known Issues

- Latency is still high
- Volcengine may return `HTTP 429` with `RequestBurstTooFast` if requests are sent too quickly
- Current backend has minimal burst retry and local cache, but this is not a full queue/rate-limit system
- Summary and outline still use source chunks rather than strict references
- Retrieval quality controls can still be improved further, but are no longer minimal
- Competition materials exist and are reusable, but still need final polish against actual submission format
- Public external sharing is only suitable for short-lived controlled demos in the current network environment

## Important Files

- Backend entry: `backend/app/main.py`
- Routes: `backend/app/api/routes.py`
- Config: `backend/app/core/config.py`
- Model client: `backend/app/services/model_client.py`
- File parsing: `backend/app/services/document_parser.py`
- Task runner: `backend/app/services/task_service.py`
- Logs: `backend/app/services/log_service.py`
- Frontend page: `frontend/src/App.tsx`
- Startup scripts:
  - `scripts/bootstrap.ps1`
  - `scripts/dev.ps1`

## How To Start

### Install dependencies

```powershell
cd C:\Users\Administrator\Desktop\project
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap.ps1
```

### Start frontend + backend

```powershell
cd C:\Users\Administrator\Desktop\project
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1
```

### Access

- Frontend: `http://localhost:5173`
- Backend docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/api/health`

## How To Verify Quickly

1. Upload a short UTF-8 `.md` file
2. Run `summary`
3. Run `ask`
4. Run `outline`
5. Check `data/logs/call_logs.jsonl`

## Tests

```powershell
cd C:\Users\Administrator\Desktop\project
.venv\Scripts\python.exe -m pytest backend/tests
```

Current status:

- `27 passed`

## Next Recommended Steps

1. Next session priority: formal online deployment
   - target architecture:
     - frontend: static site
     - backend: web service
     - backend data: persistent disk or equivalent persistent storage
   - preferred domain split:
     - main site: `yourdomain.com`
     - api: `api.yourdomain.com`
   - likely first deployment candidate: Render
   - deployment prep checklist:
     - verify frontend API base URL strategy
     - verify backend CORS origins
     - verify data directory persistence requirements for uploads / parsed / logs / cache
     - prepare environment variables for production
2. Preserve current product logic; do not start with large new feature work before deployment path is clear
3. There are currently uncommitted UI-only experiments in:
   - `frontend/src/App.tsx`
   - `frontend/src/styles.css`
   Tomorrow, decide first whether to keep, revise, or discard them before starting deployment changes
4. After deployment path is clear:
   - route-tier comparison on the real sample set
   - summary/outline stricter reference semantics
   - final submission-material polish

## Session Handoff Rule

At the start of the next session:

1. Read `WORKLOG.md`
2. Read `README.md`
3. Check `.env` exists locally
4. Check `git status --short` first, because there may be uncommitted UI experiments
5. Check recent logs in `data/logs/call_logs.jsonl`
6. Continue from the `Next Recommended Steps` section unless the user redirects

## 2026-04-16 Deployment Prep Update

- Read `WORKLOG.md`, `README.md`, local `.env` presence, `git status --short`, and recent `data/logs/call_logs.jsonl` entries before resuming work
- Confirmed there is no Git remote configured in this workspace and no local Render CLI available, so an actual cloud deploy cannot be triggered from this machine yet
- Added Render Blueprint config in `render.yaml` for:
  - static frontend service
  - Python backend service
  - persistent disk-backed backend data storage
- Added backend `DATA_DIR` env support so production uploads / parsed outputs / logs / cache can live on a persistent mount instead of the ephemeral app filesystem
- Added `frontend/.env.production.example` for `VITE_API_BASE_URL`
- Added `docs/DEPLOY_RENDER.md` with the exact remaining manual Render steps
- Normalized frontend `VITE_API_BASE_URL` handling so a trailing slash does not create malformed API URLs

### Remaining Deployment Gate

- Push repo to a Git provider that Render can access
- Create the Blueprint from `render.yaml`
- Fill the `sync: false` Render env vars:
  - `CORS_ORIGINS`
  - `WUQIONG_API_KEY`
  - `MODEL_QA`
  - `MODEL_SUMMARY`
  - `MODEL_OUTLINE`
  - `VITE_API_BASE_URL`
- If using custom domains, point:
  - frontend -> `yourdomain.com`
  - backend -> `api.yourdomain.com`
