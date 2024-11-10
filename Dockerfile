FROM python:3.12-bookworm AS base

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VERSION=1.8.3

SHELL [ "/bin/bash", "-euxo", "pipefail", "-c" ]

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true

WORKDIR /bot

ENTRYPOINT [ "/bot/docker-entrypoint.dev.sh" ]
