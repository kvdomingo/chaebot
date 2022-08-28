import os

from discord.ext.commands import Bot
from django.conf import settings

from kvisualbot.logging import logger


async def load_cogs(bot: Bot):
    for f in os.listdir(settings.BASE_DIR / "bot" / "cogs"):
        if f.endswith(".py"):
            try:
                await bot.load_extension(f"bot.cogs.{f[:-3]}")
            except Exception as e:
                logger.exception(e)


async def unload_cogs(bot: Bot):
    for f in os.listdir(settings.BASE_DIR / "bot" / "cogs"):
        if f.endswith(".py"):
            try:
                await bot.unload_extension(f"bot.cogs.{f[:-3]}")
            except Exception as e:
                logger.exception(e)
