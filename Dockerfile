FROM node:16-alpine as build

WORKDIR /web/app

COPY ./web/app ./

RUN npm install

RUN npm run build

FROM python:3.9.7-alpine as prod

RUN apk add --no-cache --update bash postgresql-dev gcc musl-dev curl

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /backend

COPY ./bot/ ./bot/
COPY ./kvisualbot/ ./kvisualbot/
COPY ./*.py ./
COPY ./*.sh ./
COPY --from=build /web/app/build ./web/app/

RUN python manage.py collectstatic --noinput

RUN adduser -D devuser

RUN mkdir ./tmp

RUN chmod -R 777 ./tmp

EXPOSE $PORT

USER devuser

CMD bash runserver.sh
