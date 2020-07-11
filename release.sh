#!/bin/bash

python manage.py dbupdate
python manage.py migrate
