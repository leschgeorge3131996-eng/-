# Aliyun Lightweight Server Deployment

This repo can be deployed on a single long-running Alibaba Cloud lightweight server.

Recommended production shape:

- one Linux server
- Nginx serves the frontend static files
- Nginx proxies `/api/*` to FastAPI on `127.0.0.1:8000`
- frontend and backend share the same public origin, so `VITE_API_BASE_URL` can stay unset

## What To Buy

On the Alibaba Cloud purchase page:

1. Do not use the `应用镜像 -> OpenClaw` image for this repo.
2. Switch to `系统镜像`.
3. Choose `Ubuntu 22.04` or `Ubuntu 24.04`.
4. Keep at least `2 vCPU / 2 GB`.
5. Open ports `22`, `80`, and `443` in the server firewall after creation.

Why not `OpenClaw`: this project is a normal `React + Vite + FastAPI` app, not an OpenClaw appliance. A plain Ubuntu image is easier to control and easier to maintain.

## Server Layout

Suggested paths:

- repo: `/opt/yandatong`
- backend venv: `/opt/yandatong/.venv`
- frontend dist: `/opt/yandatong/frontend/dist`

## 1. Install Runtime Dependencies

```bash
sudo apt update
sudo apt install -y git nginx python3 python3-venv python3-pip nodejs npm
```

## 2. Upload Or Clone The Repo

```bash
cd /opt
sudo git clone <your-repo-url> yandatong
sudo chown -R $USER:$USER /opt/yandatong
cd /opt/yandatong
```

## 3. Configure Backend Environment

Create `/opt/yandatong/.env`:

```env
APP_ENV=production
LOG_LEVEL=INFO

CORS_ORIGINS=https://your-domain.com
DATA_DIR=./data
MAX_UPLOAD_MB=20
MAX_DOCUMENT_CHARS=30000
REQUEST_TIMEOUT_SECONDS=60
DOCUMENT_RETENTION_HOURS=72
SESSION_RETENTION_HOURS=168
SESSION_COOKIE_NAME=yandatong_session
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_SAMESITE=lax
ALPHA_INVITE_CODES=alpha-demo
DEMO_MODE=false

MODEL_PROVIDER=infinigence_ai
USE_MOCK_MODEL=false
WUQIONG_BASE_URL=https://cloud.infini-ai.com/maas/v1
WUQIONG_API_KEY=your-real-key
MODEL_QA=qwen3-235b-a22b-instruct-2507
MODEL_SUMMARY=qwen3-235b-a22b-instruct-2507
MODEL_OUTLINE=qwen3-235b-a22b-instruct-2507
ROUTE_UPGRADE_CHARS=12000
```

If you are testing with the server public IP before HTTPS is ready:

- temporarily set `CORS_ORIGINS=http://<server-public-ip>`
- temporarily set `SESSION_COOKIE_SECURE=false`

## 4. Install Backend Dependencies

```bash
cd /opt/yandatong
python3 -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -r backend/requirements.txt
```

## 5. Build The Frontend

For same-origin deployment, do not set `VITE_API_BASE_URL`. The frontend will call `/api` on the same host automatically.

```bash
cd /opt/yandatong/frontend
npm ci
npm run build
```

## 6. Run FastAPI With systemd

Create `/etc/systemd/system/yandatong.service`:

```ini
[Unit]
Description=Yandatong FastAPI
After=network.target

[Service]
User=root
WorkingDirectory=/opt/yandatong
Environment=PYTHONPATH=/opt/yandatong
ExecStart=/opt/yandatong/.venv/bin/python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Then start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now yandatong
sudo systemctl status yandatong
```

## 7. Configure Nginx

Create `/etc/nginx/sites-available/yandatong`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /opt/yandatong/frontend/dist;
    index index.html;

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        try_files $uri /index.html;
    }
}
```

Enable it:

```bash
sudo ln -s /etc/nginx/sites-available/yandatong /etc/nginx/sites-enabled/yandatong
sudo nginx -t
sudo systemctl reload nginx
```

If you are using the server public IP first, replace `your-domain.com` with `_`.

## 8. Enable HTTPS

After the domain resolves to the server:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 9. Verify

Check these URLs:

- `https://your-domain.com`
- `https://your-domain.com/api/health`

Expected result:

- frontend loads normally
- `/api/health` returns JSON
- uploads and task requests work from the browser without CORS errors

## Separate Frontend / Backend Domains

Only do this if you really need it. Same-origin is simpler.

If you split domains:

- frontend: `https://your-domain.com`
- backend: `https://api.your-domain.com`

Then:

1. build frontend with `VITE_API_BASE_URL=https://api.your-domain.com/api`
2. set backend `CORS_ORIGINS=https://your-domain.com`
3. set `SESSION_COOKIE_SECURE=true`
4. set `SESSION_COOKIE_SAMESITE=none`

## Ops Notes

- this project stores uploads, parsed outputs, logs, sessions, and cache on local disk under `DATA_DIR`
- for a single-server MVP, that is acceptable
- back up `/opt/yandatong/data`
- restart commands:

```bash
sudo systemctl restart yandatong
sudo systemctl reload nginx
```
