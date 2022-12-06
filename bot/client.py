from discord import Client, Game, Intents
from discord import Object as DiscordObject
from discord import Status
from discord.app_commands import CommandTree
from django.conf import settings


class KClient(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = CommandTree(self)

        if settings.PRODUCTION:
            self.status = Status.online
            self.activity = Game(name=f"in {len(self.guilds)} servers!")
        else:
            self.status = Status.do_not_disturb
            self.activity = Game(name="under development")
        self.change_presence(status=self.status, activity=self.activity)

    async def setup_hook(self):
        if not settings.PRODUCTION:
            self.tree.copy_global_to(guild=DiscordObject(id=settings.DISCORD_TEST_GUILD_ID))
        await self.tree.sync(
            guild=DiscordObject(id=settings.DISCORD_TEST_GUILD_ID) if not settings.PRODUCTION else None
        )
