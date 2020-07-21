import os
from discord.ext import commands

import logging
logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
client = commands.Bot(command_prefix='!', description="Hi, I'm Botbot de Leon!")


def run():
    for fn in os.listdir(os.path.join(BASE_DIR, 'src', 'cogs')):
        if fn.endswith(".py"):
            client.load_extension(f"src.cogs.{fn[:-3]}")
    client.run(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    run()
