# Render Deployment

This repo is prepared for a two-service Render deployment:

- `yandatong-web`: static site for the Vite frontend
- `yandatong-api`: Python web service for the FastAPI backend

## What Was Added

- `render.yaml` to create both Render services from one Blueprint
- `DATA_DIR` support in backend config so uploads, parsed files, logs, and cache can live on a persistent disk
- `frontend/.env.production.example` to document the production API base URL
- frontend API base normalization so a trailing slash in `VITE_API_BASE_URL` does not break requests

## Before You Deploy

1. Push this repo to GitHub, GitLab, or Bitbucket.
2. Make sure the branch you want to deploy contains `render.yaml`.
3. Prepare these backend values:
   - `CORS_ORIGINS`
   - `WUQIONG_API_KEY`
   - `MODEL_QA`
   - `MODEL_SUMMARY`
   - `MODEL_OUTLINE`
4. Prepare this frontend value:
   - `VITE_API_BASE_URL`

Recommended values:

- `CORS_ORIGINS=https://your-frontend.onrender.com`
- `VITE_API_BASE_URL=https://your-api.onrender.com/api`

If you cut over to a custom domain later, temporarily include both origins in `CORS_ORIGINS` until DNS and TLS are live:

- `CORS_ORIGINS=https://your-frontend.onrender.com,https://yourdomain.com`

## Create The Services

1. In Render, create a new Blueprint and select the repo that contains this project.
2. Render will read `render.yaml` and propose two services.
3. Enter the `sync: false` variables during the initial creation flow.
4. Keep the backend disk attached at `/var/data`.
5. Deploy.

## Service Details

### Backend

- Runtime: Python
- Region: `singapore`
- Plan: `starter`
- Root directory: `backend`
- Health check: `/api/health`
- Persistent disk mount path: `/var/data`

The backend now uses `DATA_DIR`, so production writes stay under `/var/data` instead of the ephemeral repo filesystem.

### Frontend

- Runtime: Static site
- Build command: `cd frontend && npm ci && npm run build`
- Publish path: `./frontend/dist`

Set `VITE_API_BASE_URL` to the full API prefix, including `/api`.

## Custom Domains

After both services are live:

1. Add your public site domain to `yandatong-web`.
2. Add your API domain to `yandatong-api`.
3. Update `VITE_API_BASE_URL` to the final API domain.
4. Update `CORS_ORIGINS` to include the final frontend origin.

Suggested split:

- `yourdomain.com` -> frontend static site
- `api.yourdomain.com` -> backend web service

## Operational Notes

- Render persistent disks preserve only files written under the disk mount path.
- A Render service with a persistent disk cannot scale to multiple instances.
- Disk-backed deploys are not zero-downtime on Render.

Those constraints are acceptable for the current MVP because uploads, parsed outputs, logs, and cache are all local-disk based today.
