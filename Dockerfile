FROM alpine:latest as dev

RUN apk add --no-cache --update python3-dev py3-pip bash postgresql-dev gcc musl-dev screen

ADD ./requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

RUN pip3 install virtualenv

ADD . /web/app

EXPOSE 5000

RUN adduser -D devuser

USER devuser

WORKDIR /web/app

RUN python3 manage.py migrate

RUN screen -dmS api gunicorn kvisualbot.wsgi -b 0.0.0.0:$PORT --log-file -

CMD [ "python", "manage.py", "runbot" ]
