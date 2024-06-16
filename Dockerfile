# syntax=docker.io/docker/dockerfile:1.7-labs

FROM python:3.12.4-slim as base

# Pillow build requirements
# https://pillow.readthedocs.io/en/stable/installation/building-from-source.html

# The documentation asks for libjpeg8-dev, which isn't available on the slim image,
# but apt suggests libjpeg62-turbo-dev, which seems to work.
ARG pillow="libtiff5-dev libjpeg62-turbo-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev"

WORKDIR /app/

ENV PIP_DISABLE_PIP_VERSION_CHECK="on" \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  POETRY_VERSION=1.6.1

# Copy requirements first to populate Docker layer cache
COPY poetry.lock pyproject.toml /app/

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
  config/ \
  photos/ \
  static/ \
  tasks/ \
  manage.py \
  run.dev.sh \
  /app/

RUN mkdir -p /app/logs/


FROM base as development

RUN chmod +x /app/run.dev.sh


FROM node:15.12.0 AS node

WORKDIR /app/ui/

COPY \
  ui/package.json \
  ui/package-lock.json \
  ui/webpack.*.js \
  /app/
COPY ./static/ /app/static/
COPY ./ui/src/ /app/ui/src/

RUN npm ci


FROM base as staging

COPY ./config/config.staging.toml /app/config/config.toml
COPY ./config/secrets.staging.toml /app/config/secrets.toml

COPY --from=node /app/static/ /app/static/

RUN chmod +x /app/run.staging.sh


FROM base as production

COPY ./config/config.production.toml /app/config/config.toml
COPY ./config/secrets.production.toml /app/config/secrets.toml

COPY --from=node /app/static/ /app/static/

RUN poetry run python manage.py collectstatic --no-input --clear
