from discord import Client, Game, Intents, Object, Status
from discord.app_commands import CommandTree

from common.settings import settings


class KClient(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = CommandTree(self)

        if settings.IN_PRODUCTION:
            self.status = Status.online
            self.activity = Game(name=f"in {len(self.guilds)} servers!")
        else:
            self.status = Status.do_not_disturb
            self.activity = Game(name="under development")
        self.change_presence(status=self.status, activity=self.activity)

    async def setup_hook(self):
        if not settings.IN_PRODUCTION:
            self.tree.copy_global_to(guild=Object(id=settings.DISCORD_TEST_GUILD_ID))
        await self.tree.sync(
            guild=Object(id=settings.DISCORD_TEST_GUILD_ID)
            if not settings.IN_PRODUCTION
            else None
        )
