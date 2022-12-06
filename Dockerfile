FROM node:16-alpine AS build

WORKDIR /tmp

COPY ./web/app/public/ ./public/
COPY ./web/app/src/ ./src/
COPY ./web/app/package.json ./web/app/tsconfig.json ./web/app/yarn.lock ./

RUN yarn install && yarn build

FROM python:3.10-bullseye

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VERSION 1.2.2

WORKDIR /tmp

RUN apt update && apt install supervisor -y && mkdir -p /var/log/supervisor

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml ./

RUN poetry export --without-hashes -f requirements.txt | pip install --no-cache-dir -r /dev/stdin

WORKDIR /bot

COPY ./bot/ ./bot/
COPY ./kvisualbot/ ./kvisualbot/
COPY ./*.py ./
COPY supervisord.conf ./
COPY --from=build /tmp/build ./web/app/

EXPOSE $PORT

ENTRYPOINT [ "/bin/sh", \
             "-c", \
             "python manage.py collectstatic --noinput && \
              python manage.py migrate && \
              exec /usr/bin/supervisord -c /bot/supervisord.conf" ]

