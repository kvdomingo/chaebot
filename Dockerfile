FROM python:3.9.7-alpine as base

RUN apk add --no-cache --update bash postgresql-dev gcc musl-dev curl

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

FROM base as dev

WORKDIR /bot

ENTRYPOINT python main.py runbot

FROM node:16-alpine as web-dev

WORKDIR /bot

ENTRYPOINT [ "sh", "rundevserver.sh" ]

FROM base as api-dev

WORKDIR /bot

ENTRYPOINT gunicorn kvisualbot.wsgi -b 0.0.0.0:${PORT} --reload

FROM node:16-alpine as build

WORKDIR /web/app

COPY ./web/app ./

RUN yarn install

RUN yarn build

FROM base as prod

WORKDIR /bot

COPY ./bot/ ./bot/
COPY ./kvisualbot/ ./kvisualbot/
COPY ./*.py ./
COPY runserver.sh .
COPY --from=build /web/app/build ./web/app/

RUN python manage.py collectstatic --noinput

RUN adduser -D devuser

RUN mkdir ./tmp

RUN chmod -R 777 ./tmp

EXPOSE $PORT

USER devuser

CMD bash runserver.sh
