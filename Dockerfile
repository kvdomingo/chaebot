FROM alpine:latest as build

RUN apk add --no-cache --update python3-dev py3-pip bash postgresql-dev gcc musl-dev

ADD ./requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

RUN pip3 install virtualenv

COPY ./bot/ /web/app/bot/
COPY ./kvisualbot/ /web/app/kvisualbot/
COPY ./*.py /web/app/

RUN adduser -D devuser

EXPOSE $PORT

FROM build as dev

WORKDIR /web/app

RUN mkdir /web/app/tmp

ARG DEBUG
ARG SECRET_KEY
ARG DATABASE_URL
ARG PORT

ENV PYTHONUNBUFFERED 1
ENV DEBUG $DEBUG
ENV SECRET_KEY $SECRET_KEY
ENV DATABASE_URL $DATABASE_URL
ENV PORT $PORT

RUN python3 manage.py collectstatic --noinput

RUN python3 manage.py migrate

RUN chown -R devuser:devuser /web/app/tmp/

USER devuser

CMD bash -c "gunicorn kvisualbot.wsgi -b 0.0.0.0:$PORT &" && python3 main.py runbot

FROM build as prod

USER devuser

WORKDIR /web/app

CMD bash -c "gunicorn kvisualbot.wsgi -b 0.0.0.0:$PORT &" && python3 main.py runbot
