# syntax=docker/dockerfile:1.7

# ---- Stage 1: build the React/Vite frontend ----
FROM node:20-bookworm-slim AS web
WORKDIR /web
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

# ---- Stage 2: python runtime + serve frontend dist ----
FROM python:3.12-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# poppler for PDF parsing (pypdf is pure-python, but PyMuPDF + pdf rendering benefit
# from system libs); fonts-noto-cjk so any rendered text shows CJK correctly.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        fonts-noto-cjk \
        libgl1 \
        libglib2.0-0 \
        poppler-utils \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY backend /app/backend
COPY --from=web /web/dist /app/frontend/dist

# Hugging Face Spaces runs the container as UID 1000 by convention.
# Keep DATA_DIR under /data so it survives within a Space's lifetime and is writable.
RUN useradd -m -u 1000 appuser \
 && mkdir -p /data \
 && chown -R appuser:appuser /app /data
USER appuser

ENV APP_ENV=production \
    DATA_DIR=/data \
    PORT=7860

EXPOSE 7860

CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT}"]
