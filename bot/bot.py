from dotenv import load_dotenv
load_dotenv()

import os
import sentry_sdk
import logging
from django.conf import settings
from discord.ext import commands
from django.core.cache import cache
from .utils.endpoints import Api

logging.basicConfig(level=logging.INFO)

if not settings.DEBUG:
    sentry_sdk.init(
        'https://f5016ad6477147ceabb8459b73b01414@o493799.ingest.sentry.io/5563761',
        traces_sample_rate=1.0,
    )


def main():
    groups = Api.sync_groups()
    cache.set('groups', groups)

    command_prefix = '!' if settings.PYTHON_ENV == 'production' else '$'
    client = commands.Bot(command_prefix=command_prefix, description='Hi, I\'m Botbot de Leon!')
    for fn in os.listdir(settings.BASE_DIR / 'bot' / 'cogs'):
        if fn.endswith('.py'):
            client.load_extension(f'bot.cogs.{fn[:-3]}')
    client.run(os.environ.get('DISCORD_TOKEN'))


if __name__ == "__main__":
    main()
