FROM python:3.10-bullseye AS base

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VERSION 1.2.2
ENV VERSION $VERSION
ARG PORT

FROM node:16-alpine AS build

WORKDIR /web

COPY ./web/app/ ./

RUN yarn install && yarn build

FROM base as prod

RUN apt update && apt install libffi-dev libnacl-dev ffmpeg supervisor -y

RUN mkdir -p /var/log/supervisor

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /tmp

COPY poetry.lock pyproject.toml ./

RUN poetry export --without-hashes -f requirements.txt | pip install --no-cache-dir -r /dev/stdin

WORKDIR /bot

COPY ./bot/ ./bot/
COPY ./kvisualbot/ ./kvisualbot/
COPY ./*.py ./
COPY ./*.sh ./
COPY supervisord.conf ./
COPY --from=build /web/dist ./web/app/

RUN chmod +x ./docker-release.sh

EXPOSE $PORT
