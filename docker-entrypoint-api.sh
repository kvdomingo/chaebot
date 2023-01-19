#!/bin/sh

python manage.py migrate
exec gunicorn kvisualbot.wsgi --bind 0.0.0.0:5000 --config ./gunicorn.conf.py --pid /tmp/gunicorn --reload
