release: python manage.py migrate
web: gunicorn kvisualbot.wsgi --log-file -
worker: python main.py runbot
