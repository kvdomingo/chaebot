import io
import aiohttp
import discord
from discord.ext import commands


class Convenience(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong ({round(self.client.latency * 1000)}ms)')

    @commands.command(aliases=['purge', 'sanitize'])
    async def clear(self, ctx, amount: int = 0):
        if amount < 1:
            await ctx.send('Please specify a positive number.')
        else:
            await ctx.channel.purge(limit=amount + 1)

    @commands.command(aliases=['labas'])
    async def covid(self, ctx):
        img_url = 'https://res.cloudinary.com/kdphotography-assets/image/upload/v1/kvisualbot/covidph.jpg'
        async with aiohttp.ClientSession() as session:
            async with session.get(img_url) as res:
                data = io.BytesIO(await res.read())
                file = discord.File(data, 'labas.jpg')
        await ctx.send('<@696695544826953769>')
        await ctx.send(file=file)


def setup(client):
    client.add_cog(Convenience(client))
