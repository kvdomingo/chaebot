import logging

import sentry_sdk
from discord.ext import commands
from django.conf import settings
from django.core.cache import cache

from bot.api.internal import Api
from kvisualbot.logging import logger

from .utils.cog_handler import load_cogs

logging.basicConfig(level=logging.INFO)

if not settings.DEBUG:
    sentry_sdk.init(settings.SENTRY_DSN, traces_sample_rate=0.9)


def main():
    groups = Api.sync_groups()
    cache.set("groups", groups)

    command_prefix = "!" if settings.PYTHON_ENV == "production" else "$"
    client = commands.Bot(command_prefix=command_prefix, description="Hi, I'm Botbot de Leon!")
    errs = load_cogs(client)
    if len(errs) > 0:
        for e in errs:
            logger.error(e)
    client.run(settings.DISCORD_TOKEN)


if __name__ == "__main__":
    main()
