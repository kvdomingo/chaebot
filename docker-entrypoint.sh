#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate
/usr/bin/supervisord -c ./supervisord.conf
