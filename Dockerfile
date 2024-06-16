# syntax=docker.io/docker/dockerfile:1.7-labs

FROM python:3.12.4-slim as base

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
  POETRY_VERSION=1.6.1

# Copy requirements first to populate Docker layer cache
COPY \
  api/poetry.lock \
  api/pyproject.toml \
  /app/api/

RUN apt update \
  && apt install --yes $pillow \
  && pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir "poetry==$POETRY_VERSION" \
  && poetry install --no-interaction \
  && rm -rf /root/.cache/pypoetry/artifacts/ \
  && rm -rf /root/.cache/pypoetry/cache/ \
  && apt remove --yes gcc python3-dev libssl-dev $pillow \
  && apt autoremove --yes

COPY --parents \
  api/ \
  tasks/ \
  run.dev.sh \
  /app/

RUN mkdir -p /app/logs/


FROM base as backend-development

RUN chmod +x /app/run.dev.sh


FROM node:20.14.0-alpine AS frontend

WORKDIR /app/ui/

COPY ui/ /app/ui/

RUN npm install


FROM base as backend-staging

COPY ./config/config.staging.toml /app/config/config.toml
COPY ./config/secrets.staging.toml /app/config/secrets.toml

COPY --from=node /app/ui/static/ /app/ui/static/

RUN chmod +x /app/run.staging.sh


FROM base as backend-production

COPY ./config/config.production.toml /app/config/config.toml
COPY ./config/secrets.production.toml /app/config/secrets.toml

COPY --from=node /app/ui/static/ /app/ui/static/

RUN poetry run python /app/api/manage.py collectstatic --no-input --clear
