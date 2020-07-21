from discord.ext import commands


class Convenience(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong ({round(self.client.latency * 1000)}ms)')

    @commands.command()
    async def clear(self, ctx, amount: int = 0):
        if amount < 1:
            await ctx.send('Please specify a positive number.')
        else:
            await ctx.channel.purge(limit=amount + 1)


def setup(client):
    client.add_cog(Convenience(client))
