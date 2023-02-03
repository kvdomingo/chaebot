from discord import Color, Embed
from discord.ext import commands
from discord.ext.commands import Bot
from django.core.cache import cache

from ..api.internal import Api
from ..handlers.hourly import hourly_handler
from ..utils import escape_quote


class Query(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client
        self.groups = cache.get("groups") or []

    @commands.command(
        aliases=["q"],
        help="Get a random pic of the specified member from the specified group",
    )
    async def query(self, ctx, group: str, *person: str):
        person = escape_quote(person)
        response, _ = await hourly_handler(group, person)
        retries = 0
        while len(response) == 0:
            if retries == 5:
                await ctx.send("No media sources available for this group/member 😢")
                return
            response, _ = await hourly_handler(group, person)
            retries += 1

        if isinstance(response, list):
            await ctx.send(files=response)
        elif isinstance(response, str):
            await ctx.send(response)

    @commands.command(aliases=["list"], help="List all supported groups")
    async def list_(self, ctx):
        supp_groups = [group["name"] for group in Api.sync_groups()]
        for group in self.groups:
            without_source = [len(member["twitterMediaSources"]) == 0 for member in group["members"]]
            if any(without_source):
                continue
            supp_groups.append(group["name"])
        embed = Embed(
            title="Groups/artists in database:",
            description="\n".join(supp_groups),
            color=Color.green(),
        )
        await ctx.send(embed=embed)


async def setup(client: Bot):
    await client.add_cog(Query(client))
