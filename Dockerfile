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
