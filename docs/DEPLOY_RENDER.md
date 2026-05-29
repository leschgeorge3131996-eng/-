# Render Deployment

This repo deploys as **one same-origin Docker web service** on Render's free tier.

- The `Dockerfile` builds the Vite frontend, then FastAPI serves `frontend/dist`
  via the SPA fallback in `backend/app/main.py`.
- Backend and frontend share one origin, so there is no cross-origin CORS, no
  second build, and no paid plan needed.

## What `render.yaml` Declares

- A single `type: web`, `runtime: docker`, `plan: free` service named `yandatong`
- Health check at `/api/health`
- All non-secret config inline; secrets / swappable model names left as `sync: false`

## Before You Deploy

1. Push this repo to GitHub (Render reads `render.yaml` from the connected repo).
2. Make sure the deploy branch contains `render.yaml`.
3. Have these dashboard values ready (entered during Blueprint creation):
   - `WUQIONG_API_KEY` — secret, e.g. `sk-...`
   - `MODEL_QA` — `deepseek-v4-flash`
   - `MODEL_SUMMARY` — `qwen3-235b-a22b-instruct-2507`
   - `MODEL_OUTLINE` — `qwen3-235b-a22b-instruct-2507`

Everything else (provider, base URL, `DEMO_MODE=true`, limits, `CORS_ORIGINS`)
is already baked into `render.yaml`.

## The One Thing That Will Bite You

`backend/app/main.py` mounts `OriginValidationMiddleware`, a CSRF guard that
**rejects any POST/DELETE whose `Origin` is not in `CORS_ORIGINS`**. On a
same-origin deploy the browser sends the service's own `*.onrender.com` host as
the Origin, so `render.yaml` sets:

```
CORS_ORIGINS=https://*.onrender.com
```

The wildcard (supported by `backend/app/core/csrf.py`) matches whatever
subdomain Render assigns, so you do not need to know the exact URL ahead of
time. If you later attach a custom domain, add it here too:

```
CORS_ORIGINS=https://*.onrender.com,https://yourdomain.com
```

If you leave `CORS_ORIGINS` empty, uploads and asks return `403 FORBIDDEN_ORIGIN`
even though the page loads fine — the classic "it opens but the first action
fails" symptom.

## Create The Service

1. In Render: **New +** → **Blueprint** → select this repo.
2. Render reads `render.yaml` and proposes one service.
3. Fill the four `sync: false` values (`WUQIONG_API_KEY`, `MODEL_QA`,
   `MODEL_SUMMARY`, `MODEL_OUTLINE`).
4. Deploy. First Docker build takes ~10 minutes.
5. Hit `https://<service>.onrender.com/api/health` — expect `200`.
6. Open the root URL, upload the gold-sample PDF, run an ask, confirm the
   citation → PDF preview works end-to-end.

## Free-Tier Notes

- **Sleep:** the service sleeps after 15 minutes idle; the next request cold-starts
  in ~30s. Before a judged demo, hit the URL once a minute or so ahead of time to
  keep it warm.
- **No persistent disk:** `DATA_DIR=/data` is writable but ephemeral — uploads and
  logs are cleared on restart/redeploy. Acceptable for a demo where each session
  uploads fresh; do not treat it as durable storage.
- **512 MB RAM:** the Docker build runs `npm ci` + Vite build in Render's builder,
  not the runtime, so the small runtime footprint fits. If a build ever OOMs,
  pre-build `frontend/dist` locally and serve it instead.
- Users should be told to upload only non-sensitive documents.

## Demo-Day Reminder

The live URL is **supplementary** evidence ("it's deployed and reachable"). The
judged demo itself should run on the rehearsed local hot path — never cold-click
the free-tier URL in front of judges and risk a 30s spinner. See
`evidence/materials/DEFENSE_DEMO_RISK_CHECKLIST.md`.
