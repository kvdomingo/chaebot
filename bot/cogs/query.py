import discord
from random import SystemRandom
from discord.ext import commands
from django.core.cache import cache
from django.conf import settings
from ..handlers.hourly import hourly_handler
from ..utils import escape_quote

random = SystemRandom()


async def arange(count):
    for i in range(count):
        yield i


class Query(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client
        self.groups = cache.get('groups')

    @commands.command(aliases=['q'], help='Get a random pic of the specified member from the specified group')
    async def query(self, ctx, group: str, *person: str):
        person = escape_quote(person)
        response, _ = await hourly_handler(group, person)
        timeout = 0
        while not len(response):
            if timeout == 5:
                return
            response, _ = await hourly_handler(group, person)
            timeout += 1

        if isinstance(response, list):
            await ctx.send(files=response)
        elif isinstance(response, str):
            await ctx.send(response)

    @commands.command(aliases=['attack', 'hell', 'raise-hell'], hidden=True)
    async def spam(self, ctx, number: int, group: str, *person: str):
        if ctx.message.author.id != settings.DISCORD_ADMIN_ID:
            do = lambda: discord.Embed(
                    description='Sorry, only bot owner is allowed to `spam`.',
                    color=discord.Color.red(),
                )
            embed = do()
            while not embed:
                embed = do()
            await ctx.send(embed=embed)
            return
        person = escape_quote(person)
        sent = 0
        async for _ in arange(number):
            do = lambda: hourly_handler(group, person)
            response, _ = await do()
            while not response:
                response, _ = await do()
            await ctx.send(files=response)
            sent += len(response)
            if sent >= number:
                break

    @commands.command(aliases=['list'], help='List all supported groups')
    async def list_(self, ctx):
        supp_groups = []
        for group in self.groups:
            without_source = [len(member['twitterMediaSources']) == 0 for member in group['members']]
            if any(without_source):
                continue
            supp_groups.append(group['name'])
        embed = discord.Embed(
            title='Supported groups/artists:',
            description='\n'.join(supp_groups),
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Query(client))
