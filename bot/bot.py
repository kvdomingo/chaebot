import asyncio
import logging

import sentry_sdk
from discord import Intents
from discord.ext.commands import Bot
from django.conf import settings

from kvisualbot.logging import logger

from .utils.cog_handler import load_cogs

logging.basicConfig(level=logging.INFO)

if not settings.DEBUG:
    sentry_sdk.init(settings.SENTRY_DSN, traces_sample_rate=0.9)


@logger.catch
async def main():
    intents = Intents.default()
    intents.message_content = True
    bot = Bot(command_prefix=settings.BOT_PREFIX, intents=intents)
    await load_cogs(bot)
    await bot.start(settings.DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
