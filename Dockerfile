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

ENTRYPOINT [ "python", "main.py", "runbot" ]

FROM base-dev as api-dev

WORKDIR /bot

ENTRYPOINT [ "gunicorn", "kvisualbot.wsgi", "-b", "0.0.0.0:5000", "-c", "./gunicorn.conf.py", "--reload" ]

FROM node:16-alpine as build

WORKDIR /web/app

COPY ./web/app ./

RUN yarn install && yarn build

FROM base as prod

RUN apk add supervisor

RUN mkdir /var/log/supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /tmp

COPY poetry.lock pyproject.toml ./

RUN poetry export --without-hashes -f requirements.txt | pip install -r /dev/stdin

WORKDIR /bot

COPY ./bot/ ./bot/
COPY ./kvisualbot/ ./kvisualbot/
COPY ./*.py ./
COPY ./*.sh ./
COPY --from=build /web/app/build ./web/app/

RUN chmod -R 777 ./tmp

RUN chmod +x docker-entrypoint.sh

EXPOSE $PORT

ENTRYPOINT [ "/usr/bin/supervisord" ]
