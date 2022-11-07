from discord import Object as DiscordObject
from django.conf import settings

from kvisualbot.logging import logger

from ..client import KClient
from ..cogs import COMMANDS_TO_LOAD


def load_cogs(client: KClient):
    for cog in COMMANDS_TO_LOAD:
        try:
            client.tree.add_command(
                cog, guild=DiscordObject(id=settings.DISCORD_TEST_GUILD_ID) if not settings.PRODUCTION else None
            )
            logger.info(f"Loaded command/group {cog.name}")
        except Exception as e:
            logger.error(f"Failed to load command/group {cog.name}: {e}")
