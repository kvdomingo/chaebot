#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate

gunicorn kvisualbot.wsgi -b 0.0.0.0:$PORT -c ./gunicorn.conf.py
