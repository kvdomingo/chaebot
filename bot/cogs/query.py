from random import SystemRandom
from discord.ext import commands
from ..handlers.twitter import twitter_handler
from ..utils import escape_quote
from ..utils.endpoints import Api

random = SystemRandom()


class Query(commands.Cog):
    def __init__(self, client):
        self.client = client

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

    @commands.command(aliases=['list'], help='List all supported groups')
    async def list_(self, ctx):
        groups = await Api.groups()
        await ctx.send('\n'.join([group['name'] for group in groups]))


def setup(client):
    client.add_cog(Query(client))
