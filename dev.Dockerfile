FROM python:3.10-bullseye AS base

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VERSION 1.2.2
ENV VERSION $VERSION
ARG PORT

FROM base AS base-dev

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /tmp

COPY poetry.lock pyproject.toml gunicorn.conf.py ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

ENV VERSION $VERSION

FROM base-dev AS dev

WORKDIR /bot

ENTRYPOINT [ "watchmedo", "auto-restart", "--directory", "./bot/", "--recursive", "--debug-force-polling", "python", "--", "main.py", "runbot" ]

FROM base-dev as api-dev

WORKDIR /bot

ENTRYPOINT [ "gunicorn", "kvisualbot.wsgi", "--bind", "0.0.0.0:5000", "--config", "./gunicorn.conf.py", "--pid", "/tmp/gunicorn", "--reload" ]
