# syntax=docker.io/docker/dockerfile:1.7-labs

FROM python:3.12.4-slim as base

COPY --from=ghcr.io/astral-sh/uv:0.10.9 /uv /bin/

# Pillow build requirements
# https://pillow.readthedocs.io/en/stable/installation/building-from-source.html

# The documentation asks for libjpeg8-dev, which isn't available on the slim image,
# but apt suggests libjpeg62-turbo-dev, which seems to work.
ARG pillow="libtiff5-dev libjpeg62-turbo-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev"

WORKDIR /app/api/

ENV PIP_DISABLE_PIP_VERSION_CHECK="on" \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  UV_PROJECT_ENVIRONMENT="/app/venv"

COPY \
  api/uv.lock \
  api/pyproject.toml \
  api/.python-version \
  /app/api/

RUN apt update \
  && apt install --yes $pillow \
  && uv sync --frozen --no-cache \
  && apt remove --yes gcc python3-dev libssl-dev $pillow \
  && apt autoremove --yes

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

RUN npx webpack --config webpack.prod.js


FROM base as backend-staging

COPY --from=frontend-build-production /app/ui/static/ /app/api/static/

RUN chmod +x /app/run.staging.sh


FROM base as backend-production

COPY --from=frontend-build-production /app/ui/static/ /app/api/static/

RUN chmod +x /app/run.production.sh
