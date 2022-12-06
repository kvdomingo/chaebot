from discord import Color, Embed, Interaction
from discord.app_commands import Group, choices, command, describe

from ..api.internal import Api
from ..handlers.hourly import group_name_matcher
from ..utils import get_group_choices


class Twitter(Group):
    @command(name="list", description="View all hourly update subscriptions for this channel")
    async def list_(self, itx: Interaction):
        await itx.response.defer()
        groups = Api.sync_groups()
        subs_exist = list(filter(lambda x: len(x["twitterMediaSubscribedChannels"]) > 0, groups))
        subbed_groups = []
        for sub in subs_exist:
            for channel in sub["twitterMediaSubscribedChannels"]:
                if channel["channel_id"] == itx.channel.id:
                    subbed_groups.append(sub["name"])
        if len(subbed_groups):
            message = Embed(
                title="Hourly media subscriptions for this channel",
                description="\n".join(subbed_groups),
                color=Color.green(),
            )
        else:
            message = Embed(
                title="Hourly media subscriptions for this channel",
                description="None",
                color=Color.gold(),
            )
        await itx.followup.send(embed=message)

    @command(description="Subscribe to hourly updates for a group")
    @describe(group="Name or alias for a group")
    @choices(group=get_group_choices())
    async def subscribe(self, itx: Interaction, group: str):
        await itx.response.defer()
        group = await group_name_matcher(group)
        body = dict(
            channel_id=itx.channel.id,
            group=group["id"],
        )
        res, status = await Api.twitter_media_subscribed_channels(None, "post", body)
        if status == 201:
            message = Embed(
                title="Adding hourly subscription success",
                description=f'This channel has been subscribed to hourly media from {group["name"]}',
                color=Color.green(),
            )
        else:
            message = Embed(
                title="Adding hourly subscription failed",
                description="due to the following error(s):",
                color=Color.red(),
            )
            for key, val in res.items():
                message.add_field(
                    name=key,
                    value=str(val),
                    inline=False,
                )
            message.set_footer(text="Please check the errors above or try again later.")
        await itx.followup.send(embed=message)

    @command(description="Unsubscribe from hourly updates for a group")
    @describe(group="Name or alias for a group")
    @choices(group=get_group_choices())
    async def unsubscribe(self, itx: Interaction, group: str):
        await itx.response.defer()
        group = await group_name_matcher(group)
        channels = group["twitterMediaSubscribedChannels"]
        channel = list(
            filter(
                lambda x: x["channel_id"] == itx.channel.id and x["group"] == group["id"],
                channels,
            )
        )
        if channel:
            _, status = await Api.twitter_media_subscribed_channels(channel[0]["id"], "delete")
            message = Embed(
                title="Hourly media subscription removed",
                description=f'This channel has been unsubscribed from hourly media from {group["name"]}',
                color=Color.green(),
            )
        else:
            message = Embed(
                title="Hourly media subscription error",
                description=f'This channel is not subscribed to hourly media from {group["name"]}',
                color=Color.red(),
            )
        await itx.followup.send(embed=message)


twitter = Twitter()
