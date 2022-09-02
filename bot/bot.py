import asyncio
import logging

import sentry_sdk
from discord import Intents
from django.conf import settings
from django.core.cache import cache

from bot.api.internal import Api
from kvisualbot.logging import logger

from .client import KClient
from .utils.cog_handler import load_cogs

logging.basicConfig(level=logging.INFO)

if not settings.DEBUG:
    sentry_sdk.init(settings.SENTRY_DSN, traces_sample_rate=0.9)


@logger.catch
async def main():
    groups = Api.sync_groups()
    cache.set("groups", groups)
    logger.info(f"Cached {len(groups)} groups")

    intents = Intents.default()
    intents.message_content = True
    bot = KClient(intents=intents)
    load_cogs(bot)
    await bot.start(settings.DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
