import json
from .. import api
from discord.ext import commands
from discord.ext.commands import Bot, Context


class VliveApi(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client

    @commands.group(aliases=["vapi"], hidden=True)
    async def vlive_api(self, ctx):
        pass

    @vlive_api.command(help="Search groups")
    async def search(self, ctx: Context, search: str):
        channels: list = await api.vlive.search_channels(search)
        if len(channels) > 0:
            channels = list(
                filter(lambda channel: "+" not in channel["name"], channels)
            )
            channels = list(
                map(
                    lambda channel: {
                        **channel,
                        "name": channel["name"].encode("utf-16").decode("utf-16"),
                    },
                    channels,
                )
            )
            await ctx.send(json.dumps(channels, indent=2))
        else:
            await ctx.send("No results matched.")


def setup(client):
    client.add_cog(VliveApi(client))
