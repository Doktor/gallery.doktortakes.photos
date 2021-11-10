FROM python:3.6 as development

WORKDIR /app/

ENV PIP_DISABLE_PIP_VERSION_CHECK="on"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install "poetry==1.1.7"

COPY . /app/
RUN poetry install --no-interaction

RUN mkdir /app/static.1/
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
RUN /app/node_modules/webpack/bin/webpack.js --config webpack.prod.js


FROM development as staging

COPY ./data/config.staging.toml /app/data/config.toml
COPY --from=node /app/static/ /app/static/

RUN echo "Collecting static files" \
    && poetry run python manage.py collectstatic --no-input --clear \
    && echo "Successfully collected static files"


FROM staging as production

COPY ./data/config.production.toml /app/data/config.toml
