# syntax=docker.io/docker/dockerfile:1.7-labs

FROM python:3.12.4-slim as base

COPY --from=ghcr.io/astral-sh/uv:0.10.9 /uv /bin/

WORKDIR /app/api/

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  UV_PROJECT_ENVIRONMENT="/app/venv"

COPY \
  api/uv.lock \
  api/pyproject.toml \
  api/.python-version \
  /app/api/

RUN uv sync --frozen --no-cache

COPY --parents \
  api/ \
  build/ \
  tasks/ \
  run.dev.sh \
  run.staging.sh \
  run.production.sh \
  /app/

RUN mkdir -p /app/logs/


FROM base as backend-development

RUN chmod +x /app/run.dev.sh


FROM node:20.14.0-alpine AS frontend

WORKDIR /app/ui/

COPY ui/ /app/ui/

RUN npm install


FROM frontend AS frontend-build-production

WORKDIR /app/ui/

RUN npx vite build


FROM base as backend-staging

COPY --from=frontend-build-production /app/ui/static/ /app/api/static/

RUN chmod +x /app/run.staging.sh


FROM base as backend-production

COPY --from=frontend-build-production /app/ui/static/ /app/api/static/

RUN chmod +x /app/run.production.sh
