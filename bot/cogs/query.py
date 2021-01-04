import os
import discord
from random import SystemRandom
from discord.ext import commands
from django.core.cache import cache
from ..handlers.twitter import twitter_handler
from ..utils import escape_quote
from ..utils.endpoints import Api

random = SystemRandom()


async def arange(count):
    for i in range(count):
        yield i


class Query(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.groups = cache.get('groups')

    @commands.command(aliases=['q'], help='Get a random member pic from the specified group')
    async def query(self, ctx, group: str, *person: str):
        person = escape_quote(person)
        response, _ = await twitter_handler(group, person)
        timeout = 0
        while not len(response):
            if timeout == 5:
                return
            response, _ = await twitter_handler(group, person)
            timeout += 1

        if isinstance(response, list):
            await ctx.send(files=response)
        elif isinstance(response, str):
            await ctx.send(response)

    @commands.command()
    async def spam(self, ctx, number: int, group: str, *person: str):
        if str(ctx.message.author.id) != os.environ.get('DISCORD_ADMIN_ID'):
            embed = discord.Embed(
                description='Sorry, only bot owner is allowed to `spam`.',
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return
        person = escape_quote(person)
        sent = 0
        async for _ in arange(number):
            response, _ = await twitter_handler(group, person)
            await ctx.send(files=response)
            sent += len(response)
            if sent >= number:
                break

    @commands.command(aliases=['list'], help='List all supported groups')
    async def list_(self, ctx):
        await ctx.send('\n'.join([group['name'] for group in self.groups]))


def setup(client):
    client.add_cog(Query(client))
