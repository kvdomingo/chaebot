import discord
from discord.ext import commands
from discord.ext.commands import Bot
from django.conf import settings

from kvisualbot.logging import logger


class Startup(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Logged in as {self.client.user}")
        if settings.IN_PRODUCTION:
            activity_name = f"in {len(self.client.guilds)} servers!"
            status = discord.Status.online
        else:
            activity_name = "under development"
            status = discord.Status.do_not_disturb
        await self.client.change_presence(
            status=status, activity=discord.Game(name=activity_name)
        )


async def setup(client: Bot):
    await client.add_cog(Startup(client))
