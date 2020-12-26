from django import db
from random import SystemRandom
from discord.ext import commands
from ..handlers.twitter import twitter_handler
from ..utils import escape_quote
from ..models import Group
from ..serializers import GroupSerializer

random = SystemRandom()


class Query(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.groups = GroupSerializer(Group.objects.all(), many=True).data

    @commands.command(aliases=['q'], help='Get a random member pic from the specified group')
    async def query(self, ctx, group: str, *person: str):
        person = escape_quote(person)
        response = await twitter_handler(group, person)
        while not len(response):
            response = await twitter_handler(group, person)

        if isinstance(response, list):
            await ctx.send(files=response)
        elif isinstance(response, str):
            await ctx.send(response)
        db.close_old_connections()

    @commands.command(aliases=['list'], help='List all supported groups')
    async def list_(self, ctx):
        ctx.send('\n'.join([group['name'] for group in self.groups]))


def setup(client):
    client.add_cog(Query(client))
