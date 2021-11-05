#!/bin/bash

python manage.py migrate
bash -c "gunicorn kvisualbot.wsgi -b 0.0.0.0:${PORT} &"
python main.py runbot
