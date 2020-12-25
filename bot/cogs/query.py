from random import SystemRandom
from discord.ext import commands
from ..utils import query_handler
from ..models import Group

random = SystemRandom()


class Query(commands.Cog):
    def __init__(self, client):
        self.client = client

        groups = Group.objects.all()
