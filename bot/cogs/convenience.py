from discord.ext import commands
from discord.ext.commands import Bot, Context


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
            await ctx.channel.purge(limit=amount + 1)


async def setup(client: Bot):
    await client.add_cog(Convenience(client))
