FROM python:3.10 as base

WORKDIR /app/

ENV PIP_DISABLE_PIP_VERSION_CHECK="on" \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  POETRY_VERSION=1.1.13

RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"

# Copy requirements first to populate Docker layer cache
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-interaction

COPY . /app/

RUN mkdir -p /app/logs/


FROM base as development

RUN chmod +x /app/run.dev.sh


FROM node:15.12.0 AS node

WORKDIR /app/

COPY \
  package.json \
  package-lock.json \
  webpack.*.js \
  /app/
COPY ./src/ /app/src/

RUN npm ci
RUN npx webpack --config webpack.prod.js


FROM base as staging

COPY ./config/config.staging.toml /app/config/config.toml
COPY ./config/secrets.staging.toml /app/config/secrets.toml

COPY --from=node /app/static/ /app/static/

RUN chmod +x /app/run.staging.sh && \
    chmod +x /app/run-celery.staging.sh


FROM base as production

COPY ./config/config.production.toml /app/config/config.toml
COPY ./config/secrets.production.toml /app/config/secrets.toml

COPY --from=node /app/static/ /app/static/

RUN poetry run python manage.py collectstatic --no-input --clear
