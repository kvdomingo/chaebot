import os
from src import BASE_DIR
from discord.ext import commands

import logging
logging.basicConfig(level=logging.INFO)

client = commands.Bot(command_prefix='!', description="Hi, I'm Botbot de Leon!")


def run():
    for fn in os.listdir(BASE_DIR / 'src' / 'cogs'):
        if fn.endswith(".py"):
            client.load_extension(f"src.cogs.{fn[:-3]}")
    client.run(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    run()
