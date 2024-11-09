from discord.ext import commands
from discord.ext.commands import Bot, Context

from common.settings import settings


class Convenience(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client

    @commands.command()
    async def ping(self, ctx: Context):
        await ctx.send(f"Pong ({round(self.client.latency * 1000)}ms)")

    @commands.command(aliases=["clear"])
    async def purge(self, ctx: Context, amount: int = 0):
        if amount < 1:
            await ctx.send("Please specify a positive number.")
        else:
            await ctx.channel.purge(
                limit=min(amount + 1, settings.DISCORD_MESSAGE_PURGE_LIMIT)
            )


async def setup(client: Bot):
    await client.add_cog(Convenience(client))
