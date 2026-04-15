# WORKLOG

## Project

- Name: `研答通`
- Goal: build a document assistant MVP with upload, cloud-model processing, result display, and local logs.
- Principle: first make the smallest runnable loop, then enhance step by step.

## Current Status

- Phase: `P0 / MVP`
- Status: `running end-to-end`
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

### Verified Results

- Frontend upload works
- `summary` works with real model
- `ask` works with real model
- `outline` works with real model
- API docs page works
- Call logs are written locally
- Backend tests pass: `10 passed`
- Log summary exported to `evidence/reports/latest_log_summary.md`

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
- Real call logs contain:
  - `model_name`
  - `success`
  - `latency_ms`
  - `token_in / token_out / token_total`

## Known Issues

- Latency is still high
- Volcengine may return `HTTP 429` with `RequestBurstTooFast` if requests are sent too quickly
- Current backend has minimal burst retry and local cache, but this is not a full queue/rate-limit system
- Summary and outline still do not return structured references
- Retrieval quality controls still need stronger scoring/ordering
- Competition materials are still missing finalized written assets

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

- `15 passed`

## Next Recommended Steps

1. Start phase 2 in this order:
   - stronger retrieval scoring and ordering
2. Finalize first version of competition materials:
   - one-page project summary
   - demo script
   - sample set
   - architecture note

## Session Handoff Rule

At the start of the next session:

1. Read `WORKLOG.md`
2. Read `README.md`
3. Check `.env` exists locally
4. Check recent logs in `data/logs/call_logs.jsonl`
5. Continue from the `Next Recommended Steps` section unless the user redirects
