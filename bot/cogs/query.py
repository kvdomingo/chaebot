from random import SystemRandom
from discord.ext import commands
from ..handlers.twitter import twitter_handler
from ..utils import escape_quote
from ..utils.group import group_name_matcher
from ..models import Group

random = SystemRandom()


class Query(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.groups = Group.objects.all()

    @commands.command(aliases=['q'], help='Get a random member pic from the specified group')
    async def query(self, ctx, group: str, *person: str):
        group = await group_name_matcher(group)
        person = escape_quote(person)
        response = await twitter_handler(group, person)
        while not len(response):
            response = await twitter_handler(group, person)

        if isinstance(response, list):
            await ctx.send(files=response)
            # await bombard_hearts(message)
        elif isinstance(response, str):
            await ctx.send(response)

    @commands.command(aliases=['list'], help='List all supported groups')
    async def list_(self, ctx):
        ctx.send('\n'.join([group.name for group in self.groups]))


def setup(client):
    client.add_cog(Query(client))
