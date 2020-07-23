from discord.ext import commands
from src.crud import *


class Subscription(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(hidden=True)
    async def twitter(self, ctx):
        pass

    @twitter.command(aliases=['subscribe', 'sub'], help='Subscribe the channel to hourly updates of the selected group')
    async def twitter_subscribe(self, ctx, group: str):
        message = TwitterChannelApi().create(ctx.channel.id, group)
        await ctx.send(message)

    @twitter.command(aliases=['unsubscribe', 'usub'], help='Unsubscribe the channel to any hourly update')
    async def twitter_unsubscribe(self, ctx, group: str):
        message = TwitterChannelApi().delete(ctx.channel.id, group)
        await ctx.send(message)

    @commands.group(hidden=True)
    async def vlive(self, ctx):
        pass

    @vlive.command(aliases=['subscribe', 'sub'], help='Subscribe the channel to VLIVE notifications of the selected group')
    async def vlive_subscribe(self, ctx, name: str):
        message = VliveChannelApi().create(ctx.channel.id, name)
        await ctx.send(message)

    @vlive.command(aliases=['unsubscribe', 'usub'], help='Unsubscribe the channel to VLIVE notifications of the selected group')
    async def vlive_unsubscribe(self, ctx):
        message = VliveChannelApi().delete(ctx.channel.id)
        await ctx.send(message)


def setup(client):
    client.add_cog(Subscription(client))
