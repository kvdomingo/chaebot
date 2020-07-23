from random import SystemRandom
from discord.ext import commands
from src.utils import bombard_hearts, query_handler


random = SystemRandom()


class Query(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help='Get a random pic from a random JYP group')
    async def jyp(self, ctx):
        group = random.choice([self.itzy, self.twice])
        await group(ctx, '')

    @commands.command(aliases=['pink', 'mink', 'bp'], help='Get a random pic of the specified BLACKPINK member')
    async def blackpink(self, ctx, *person: str):
        group = 'blackpink'
        await query_handler(ctx, group, person)

    @commands.command(aliases=['bangtan'], help='Get a random pic of the specified BTS member')
    async def bts(self, ctx, *person: str):
        group = 'bts'
        await query_handler(ctx, group, person)

    @commands.command(aliases=['itz'], help='Get a random pic of the specified ITZY member')
    async def itzy(self, ctx, *person: str):
        group = 'itzy'
        await query_handler(ctx, group, person)

    @commands.command(help='Get a random pic of IU')
    async def iu(self, ctx, *person: str):
        group = 'iu'
        await query_handler(ctx, group, person)

    @commands.command(aliases=['mama'], help='Get a random pic of the specified MAMAMOO member')
    async def mamamoo(self, ctx, *person: str):
        group = 'mamamoo'
        await query_handler(ctx, group, person)

    @commands.command(
        aliases=['red-velvet', 'red', 'velvet', 'rv', 'reve'],
        help='Get a random pic of the specified RED VELVET member'
    )
    async def red_velvet(self, ctx, *person: str):
        group = 'redvelvet'
        await query_handler(ctx, group, person)

    @commands.command(help='Get a random pic of Somi')
    async def somi(self, ctx, *person: str):
        group = 'somi'
        await query_handler(ctx, group, person)

    @commands.command(aliases=['more'], help='Get a random pic of the specified TWICE member')
    async def twice(self, ctx, *person: str):
        group = 'twice'
        await query_handler(ctx, group, person)


def setup(client):
    client.add_cog(Query(client))
