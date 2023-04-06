import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context
from django.core.cache import cache

from ..api.internal import Api
from ..handlers.hourly import group_name_matcher


class Twitter(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.groups = cache.get("groups")

    @commands.group(hidden=True)
    async def twitter(self, ctx: Context):
        pass

    @twitter.command(aliases=["list"], help="List all twitter subscriptions for the channel")
    async def list_(self, ctx: Context):
        subs_exist = list(filter(lambda x: len(x["twitterMediaSubscribedChannels"]) > 0, self.groups))
        subbed_groups = []
        for sub in subs_exist:
            for channel in sub["twitterMediaSubscribedChannels"]:
                if channel["channel_id"] == ctx.channel.id:
                    subbed_groups.append(sub["name"])
        if len(subbed_groups):
            message = discord.Embed(
                title="Hourly media subscriptions for this channel",
                description="\n".join(subbed_groups),
                color=discord.Color.green(),
            )
        else:
            message = discord.Embed(
                title="Hourly media subscriptions for this channel",
                description="None",
                color=discord.Color.gold(),
            )
        await ctx.send(embed=message)

    @twitter.command(
        aliases=["subscribe", "sub"],
        help="Subscribe the channel to twitter updates of the selected group",
    )
    async def subscribe(self, ctx: Context, group: str):
        group = await group_name_matcher(group)
        body = dict(
            channel_id=ctx.channel.id,
            group=group["id"],
        )
        res = await Api.twitter_media_subscribed_channels(None, "post", body)
        data = await res.json()
        if res.ok:
            message = discord.Embed(
                title="Adding twitter subscription success",
                description=f'This channel has been subscribed to twitter media from {group["name"]}',
                color=discord.Color.green(),
            )
        else:
            message = discord.Embed(
                title="Adding twitter subscription failed",
                description="due to the following error(s):",
                color=discord.Color.red(),
            )
            for key, val in data.items():
                message.add_field(
                    name=key,
                    value=str(val),
                    inline=False,
                )
            message.set_footer(text="Please check the errors above or try again later.")
        await ctx.send(embed=message)

    @twitter.command(
        aliases=["unsubscribe", "usub"],
        help="Unsubscribe the channel to any twitter update",
    )
    async def unsubscribe(self, ctx: Context, group: str):
        group = await group_name_matcher(group)
        channels = group["twitterMediaSubscribedChannels"]
        channel = list(
            filter(
                lambda x: x["channel_id"] == ctx.channel.id and x["group"] == group["id"],
                channels,
            )
        )
        if channel:
            await Api.twitter_media_subscribed_channels(channel[0]["id"], "delete")
            message = discord.Embed(
                title="Hourly media subscription removed",
                description=f'This channel has been unsubscribed from twitter media from {group["name"]}',
                color=discord.Color.green(),
            )
        else:
            message = discord.Embed(
                title="Hourly media subscription error",
                description=f'This channel is not subscribed to twitter media from {group["name"]}',
                color=discord.Color.red(),
            )
        await ctx.send(embed=message)


async def setup(client: Bot):
    await client.add_cog(Twitter(client))
