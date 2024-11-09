import asyncio
import logging

from discord import Intents
from discord.ext.commands import Bot
from loguru import logger

from common.settings import settings

from .utils.cog_handler import load_cogs

logging.basicConfig(level=logging.INFO)


@logger.catch
async def main():
    intents = Intents.default()
    intents.message_content = True
    bot = Bot(command_prefix=settings.BOT_PREFIX, intents=intents)
    await load_cogs(bot)
    await bot.start(settings.DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
