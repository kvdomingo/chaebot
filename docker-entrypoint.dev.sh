#!/usr/bin/env bash

set -euxo pipefail

poetry install --no-root --with dev
poetry run alembic upgrade head

exec poetry run watchmedo auto-restart --directory ./bot/ --directory ./common/ --recursive -- python -- -m bot
