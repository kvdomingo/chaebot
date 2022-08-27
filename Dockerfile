FROM python:3.10-bullseye as base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONHASHSEED random
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PIP_DEFAULT_TIMEOUT 100
ENV POETRY_VERSION 1.1.13
ENV VERSION $VERSION
ARG PORT

FROM base as base-dev

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml gunicorn.conf.py ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

ENV VERSION $VERSION

FROM base-dev as dev

WORKDIR /bot

ENTRYPOINT [ "watchmedo", "auto-restart", "-d", "./bot/", "-R", "--debug-force-polling", "python", "--", "main.py", "runbot" ]

FROM base-dev as api-dev

WORKDIR /bot

ENTRYPOINT [ "gunicorn", "kvisualbot.wsgi", "-b", "0.0.0.0:5000", "-c", "./gunicorn.conf.py", "--reload" ]

FROM node:16-alpine as build

WORKDIR /web

COPY ./web/app/public/ ./public/
COPY ./web/app/src/ ./src/
COPY ./web/app/package.json ./web/app/tsconfig.json ./web/app/yarn.lock ./

RUN yarn install && yarn build

FROM base as prod

RUN apt update && apt install supervisor -y

RUN mkdir -p /var/log/supervisor

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /tmp

COPY poetry.lock pyproject.toml ./

RUN poetry export --without-hashes -f requirements.txt | pip install -r /dev/stdin

WORKDIR /bot

COPY ./bot/ ./bot/
COPY ./kvisualbot/ ./kvisualbot/
COPY ./*.py ./
COPY ./*.sh ./
COPY supervisord.conf ./
COPY --from=build /web/build ./web/app/

RUN chmod +x docker-entrypoint.sh

EXPOSE $PORT

ENTRYPOINT [ "/usr/bin/supervisord", "-c", "supervisord.conf" ]
