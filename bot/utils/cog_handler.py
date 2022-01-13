import os
from pathlib import Path
from django.conf import settings
from discord.ext.commands import Bot

BASE_DIR: Path = settings.BASE_DIR


def load_cogs(client: Bot) -> list:
    errs = []
    for f in os.listdir(BASE_DIR / "bot" / "cogs"):
        if f.endswith(".py"):
            try:
                client.load_extension(f"bot.cogs.{f[:-3]}")
            except Exception as e:
                errs.append(str(e))
                continue
    return errs


def unload_cogs(client: Bot) -> list:
    errs = []
    for f in os.listdir(BASE_DIR / "bot" / "cogs"):
        if f.endswith(".py"):
            try:
                client.unload_extension(f"bot.cogs.{f[:-3]}")
            except Exception as e:
                errs.append(str(e))
                continue
    return errs


def reload_cogs(client: Bot) -> list:
    return [*unload_cogs(client), *load_cogs(client)]
