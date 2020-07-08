#!/bin/bash

python manage.py migrate
python backend/update_models.py
