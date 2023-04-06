import asyncio
import logging

from discord import Intents
from django.conf import settings

from bot.client import KBot
from bot.utils.cog_handler import load_cogs
from kvisualbot.logging import logger

logging.basicConfig(level=logging.INFO)


@logger.catch
async def main():
    intents = Intents.default()
    intents.message_content = True
    bot = KBot(command_prefix=settings.BOT_PREFIX, intents=intents)
    await load_cogs(bot)
    await bot.start(settings.DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
