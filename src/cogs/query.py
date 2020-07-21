from random import SystemRandom
from discord.ext import commands
from src.utils import bombard_hearts, escape_quote
from src.handlers.twitter import media_handler as twitter_handler


random = SystemRandom()


class Query(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help='Get a random pic from a random JYP group')
    async def jyp(self, ctx):
        group = random.choice([self.itzy, self.twice])
        await group(ctx, '')

    @commands.command(aliases=['itz'], help='Get a random pic of the specified ITZY member')
    async def itzy(self, ctx, *person: str):
        person = escape_quote(person)
        group = 'itzy'
        media = await twitter_handler(group, person)
        message = await ctx.send(files=media)
        await bombard_hearts(message)

    @commands.command(aliases=['pink', 'mink', 'bp'], help='Get a random pic of the specified BLACKPINK member')
    async def blackpink(self, ctx, *person: str):
        person = escape_quote(person)
        group = 'blackpink'
        media = await twitter_handler(group, person)
        message = await ctx.send(files=media)
        await bombard_hearts(message)

    @commands.command(aliases=['more'], help='Get a random pic of the specified TWICE member')
    async def twice(self, ctx, *person: str):
        person = escape_quote(person)
        group = 'twice'
        media = await twitter_handler(group, person)
        message = await ctx.send(files=media)
        await bombard_hearts(message)

    @commands.command(
        aliases=['red-velvet', 'red', 'velvet', 'rv'],
        help='Get a random pic of the specified RED VELVET member'
    )
    async def red_velvet(self, ctx, *person: str):
        person = escape_quote(person)
        group = 'redvelvet'
        media = await twitter_handler(group, person)
        message = await ctx.send(files=media)
        await bombard_hearts(message)

    @commands.command(help='Get a random pic of IU')
    async def iu(self, ctx, *person: str):
        person = escape_quote(person)
        group = 'iu'
        media = await twitter_handler(group, person)
        message = await ctx.send(files=media)
        await bombard_hearts(message)

    @commands.command(aliases=['bangtan'], help='Get a random pic of the specified BTS member')
    async def bts(self, ctx, *person: str):
        person = escape_quote(person)
        group = 'bts'
        media = await twitter_handler(group, person)
        message = await ctx.send(files=media)
        await bombard_hearts(message)

    @commands.command(aliases=['mama'], help='Get a random pic of the specified MAMAMOO member')
    async def mamamoo(self, ctx, *person: str):
        person = escape_quote(person)
        group = 'mamamoo'
        media = await twitter_handler(group, person)
        message = await ctx.send(files=media)
        await bombard_hearts(message)


def setup(client):
    client.add_cog(Query(client))
