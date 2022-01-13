import discord
from discord.ext import commands
from django.core.cache import cache
from .. import api
from ..api.internal import Api
from ..handlers.hourly import group_name_matcher


class Subscription(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.groups = cache.get("groups")

    @commands.group(hidden=True)
    async def hourly(self, ctx):
        pass

    @hourly.command(
        aliases=["list"], help="List all hourly subscriptions for the channel"
    )
    async def hourly_list(self, ctx):
        subs_exist = list(
            filter(lambda x: len(x["twitterMediaSubscribedChannels"]) > 0, self.groups)
        )
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

    @hourly.command(
        aliases=["subscribe", "sub"],
        help="Subscribe the channel to hourly updates of the selected group",
    )
    async def hourly_subscribe(self, ctx, group: str):
        group = await group_name_matcher(group)
        body = dict(
            channel_id=ctx.channel.id,
            group=group["id"],
        )
        res, status = await Api.twitter_media_subscribed_channels(None, "post", body)
        if status == 201:
            message = discord.Embed(
                title="Adding hourly subscription success",
                description=f'This channel has been subscribed to hourly media from {group["name"]}',
                color=discord.Color.green(),
            )
        else:
            message = discord.Embed(
                title="Adding hourly subscription failed",
                description="due to the following error(s):",
                color=discord.Color.red(),
            )
            for key, val in res.items():
                message.add_field(
                    name=key,
                    value=str(val),
                    inline=False,
                )
            message.set_footer(text="Please check the errors above or try again later.")
        await ctx.send(embed=message)

    @hourly.command(
        aliases=["unsubscribe", "usub"],
        help="Unsubscribe the channel to any hourly update",
    )
    async def twitter_unsubscribe(self, ctx, group: str):
        group = await group_name_matcher(group)
        channels = group["twitterMediaSubscribedChannels"]
        channel = list(
            filter(
                lambda x: x["channel_id"] == ctx.channel.id
                and x["group"] == group["id"],
                channels,
            )
        )
        if channel:
            _, status = await Api.twitter_media_subscribed_channels(
                channel[0]["id"], "delete"
            )
            message = discord.Embed(
                title="Hourly media subscription removed",
                description=f'This channel has been unsubscribed from hourly media from {group["name"]}',
                color=discord.Color.green(),
            )
        else:
            message = discord.Embed(
                title="Hourly media subscription error",
                description=f'This channel is not subscribed to hourly media from {group["name"]}',
                color=discord.Color.red(),
            )
        await ctx.send(embed=message)

    @commands.group(hidden=True)
    async def vlive(self, ctx):
        pass

    @vlive.command(
        aliases=["list"], help="List all VLIVE subscriptions for the channel"
    )
    async def vlive_list(self, ctx):
        subs_exist = list(
            filter(lambda x: len(x["vliveSubscribedChannels"]) > 0, self.groups)
        )
        subbed_groups = []
        for sub in subs_exist:
            for channel in sub["vliveSubscribedChannels"]:
                if channel["channel_id"] == ctx.channel.id:
                    subbed_groups.append(sub["name"])
        if len(subbed_groups):
            message = discord.Embed(
                title="VLIVE subscriptions for this channel",
                description="\n".join(subbed_groups),
                color=discord.Color.green(),
            )
        else:
            message = discord.Embed(
                title="VLIVE subscriptions for this channel",
                description="None",
                color=discord.Color.gold(),
            )
        await ctx.send(embed=message)

    @vlive.command(
        aliases=["subscribe", "sub"],
        help="Subscribe the channel to VLIVE notifications of the selected group",
    )
    async def vlive_subscribe(self, ctx, group: str):
        matched_group = await group_name_matcher(group, random_on_no_match=False)
        if len(matched_group.values()) == 0:
            channels: list = await api.vlive.search_channels(group)
            if len(channels) == 1:
                Api.group()
        else:
            body = dict(
                channel_id=ctx.channel.id,
                group=matched_group["id"],
            )
            res, status = await Api.vlive_subscribed_channels(None, "post", body)
            if status == 201:
                message = discord.Embed(
                    title="Adding VLIVE subscription success",
                    description=f'This channel has been subscribed to VLIVE updates from {matched_group["name"]}',
                    color=discord.Color.green(),
                )
            else:
                message = discord.Embed(
                    title="Adding VLIVE subscription failed",
                    description="due to the following error(s):",
                    color=discord.Color.red(),
                )
                for key, val in res.items():
                    message.add_field(
                        name=key,
                        value=str(val),
                        inline=False,
                    )
                message.set_footer(
                    text="Please check the errors above or try again later."
                )
            await ctx.send(embed=message)

    @vlive.command(
        aliases=["unsubscribe", "usub"],
        help="Unsubscribe the channel to VLIVE notifications of the selected group",
    )
    async def vlive_unsubscribe(self, ctx, group: str):
        group = await group_name_matcher(group)
        channels = group["vliveSubscribedChannels"]
        channel = list(
            filter(
                lambda x: x["channel_id"] == ctx.channel.id
                and x["group"] == group["id"],
                channels,
            )
        )
        if channel:
            _, status = await Api.vlive_subscribed_channels(channel[0]["id"], "delete")
            message = discord.Embed(
                title="VLIVE subscription removed",
                description=f'This channel has been unsubscribed from VLIVE updates from {group["name"]}',
                color=discord.Color.green(),
            )
        else:
            message = discord.Embed(
                title="VLIVE subscription error",
                description=f'This channel is not subscribed to VLIVE updates from {group["name"]}',
                color=discord.Color.red(),
            )
        await ctx.send(embed=message)


def setup(client):
    client.add_cog(Subscription(client))
