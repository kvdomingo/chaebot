from discord import Client, Intents
from discord import Object as DiscordObject
from discord.app_commands import CommandTree
from django.conf import settings


class KClient(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = CommandTree(self)

    async def setup_hook(self):
        if not settings.PRODUCTION:
            self.tree.copy_global_to(guild=DiscordObject(id=settings.DISCORD_TEST_GUILD_ID))
        await self.tree.sync(
            guild=DiscordObject(id=settings.DISCORD_TEST_GUILD_ID) if not settings.PRODUCTION else None
        )
