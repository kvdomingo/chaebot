from discord.ext.commands import Bot
from django.conf import settings

from kvisualbot.logging import logger


async def load_cogs(bot: Bot):
    for f in (settings.BASE_DIR / "bot" / "cogs").glob("*.py"):
        if f.name.startswith("_"):
            continue
        try:
            await bot.load_extension(f"bot.cogs.{f.stem}")
        except Exception as e:
            logger.exception(e)


async def unload_cogs(bot: Bot):
    for f in (settings.BASE_DIR / "bot" / "cogs").glob("*.py"):
        if f.name.startswith("_"):
            continue
        try:
            await bot.unload_extension(f"bot.cogs.{f.stem}")
        except Exception as e:
            logger.exception(e)
