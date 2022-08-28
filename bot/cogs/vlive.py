import vlive
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot, Context


class VliveApi(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client

    @commands.group(aliases=["vapi"], hidden=True)
    async def vlive_api(self, ctx):
        pass

    @vlive_api.command(help="Search groups")
    async def search(self, ctx: Context, search: str = ""):
        if not search:
            return await ctx.send("Error: missing search query")
        channels = vlive.search.channels(search)
        if len(channels) > 0:
            channels = [channel for channel in channels if "+" not in channel.name]
            message = Embed(title=f'Search results for "{search}"')
            for channel in channels:
                message.add_field(name=channel.name, value=channel.code, inline=False)
            await ctx.send(embed=message)
        else:
            await ctx.send("No results matched.")


async def setup(client):
    await client.add_cog(VliveApi(client))
