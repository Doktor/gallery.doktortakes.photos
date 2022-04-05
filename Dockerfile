FROM python:3.6 as development

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


FROM development as staging

COPY ./data/config.staging.toml /app/data/config.toml
COPY --from=node /app/static/ /app/static/

RUN echo "Collecting static files" \
    && poetry run python manage.py collectstatic --no-input --clear \
    && echo "Successfully collected static files"


FROM staging as production

COPY ./data/config.production.toml /app/data/config.toml
