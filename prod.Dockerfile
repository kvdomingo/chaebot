FROM python:3.10-bullseye AS prod

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VERSION 1.3.2
ENV VERSION $VERSION
ARG PORT

RUN apt update && apt install supervisor -y

RUN mkdir -p /var/log/supervisor

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /tmp

COPY poetry.lock pyproject.toml ./

RUN poetry export --without-hashes -f requirements.txt | pip install --no-cache-dir -r /dev/stdin

WORKDIR /bot

COPY ./bot/ ./bot/
COPY ./kvisualbot/ ./kvisualbot/
COPY ./*.py ./
COPY ./*.sh ./
COPY supervisord.conf ./

RUN python manage.py collectstatic --noinput

RUN chmod +x ./docker-release.sh

EXPOSE $PORT
