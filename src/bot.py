import os
import sentry_sdk
import logging
from src import BASE_DIR, DEBUG
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

if not DEBUG:
    sentry_sdk.init(
        "https://f5016ad6477147ceabb8459b73b01414@o493799.ingest.sentry.io/5563761",
        traces_sample_rate=1.0,
    )

client = commands.Bot(command_prefix='$', description="Hi, I'm Botbot de Leon!")


def run():
    for fn in os.listdir(BASE_DIR / 'src' / 'cogs'):
        if fn.endswith(".py"):
            client.load_extension(f"src.cogs.{fn[:-3]}")
    client.run(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    run()
