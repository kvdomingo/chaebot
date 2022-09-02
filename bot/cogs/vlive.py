import vlive
from discord import Color, Embed, Interaction
from discord.app_commands import Group, choices, command, describe
from django.core.cache import cache

from ..api.internal import Api
from ..handlers.hourly import api, group_name_matcher
from ..utils import get_group_choices


class Vlive(Group):
    @command(description="Search for a group name using the VLIVE API")
    async def search(self, itx: Interaction, search: str = ""):
        if not search:
            return await itx.response.send_message("Error: missing search query")
        channels = vlive.search.channels(search)
        if len(channels) > 0:
            channels = [channel for channel in channels if "+" not in channel.name]
            message = Embed(title=f'Search results for "{search}"')
            for channel in channels:
                message.add_field(name=channel.name, value=channel.code, inline=False)
            await itx.response.send_message(embed=message)
        else:
            await itx.response.send_message("No results matched.")

    @command(name="list", description="List all VLIVE subscriptions for the channel")
    async def list_(self, itx: Interaction):
        groups = cache.get("groups") or []
        subs_exist = list(filter(lambda x: len(x["vliveSubscribedChannels"]) > 0, groups))
        subbed_groups = []
        for sub in subs_exist:
            for channel in sub["vliveSubscribedChannels"]:
                if channel["channel_id"] == itx.channel.id:
                    subbed_groups.append(sub["name"])
        if len(subbed_groups):
            message = Embed(
                title="VLIVE subscriptions for this channel",
                description="\n".join(subbed_groups),
                color=Color.green(),
            )
        else:
            message = Embed(
                title="VLIVE subscriptions for this channel",
                description="None",
                color=Color.gold(),
            )
        await itx.response.send_message(embed=message)

    @command(description="Subscribe to notifications when a group goes live")
    @describe(group="Name or alias for a group")
    @choices(group=get_group_choices())
    async def subscribe(self, itx: Interaction, group: str):
        matched_group = await group_name_matcher(group, random_on_no_match=False)
        if len(matched_group.values()) == 0:
            channels: list = await api.vlive.search_channels(group)
            if len(channels) == 1:
                await Api.group()
        else:
            body = dict(
                channel_id=itx.channel.id,
                group=matched_group["id"],
            )
            res, status = await Api.vlive_subscribed_channels(None, "post", body)
            if status == 201:
                message = Embed(
                    title="Adding VLIVE subscription success",
                    description=f'This channel has been subscribed to VLIVE updates from {matched_group["name"]}',
                    color=Color.green(),
                )
            else:
                message = Embed(
                    title="Adding VLIVE subscription failed",
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
            await itx.response.send_message(embed=message)

    @command(description="Unsubscribe from notifications when a group goes live")
    @describe(group="Name or alias for a group")
    @choices(group=get_group_choices())
    async def vlive_unsubscribe(self, itx: Interaction, group: str):
        group = await group_name_matcher(group)
        channels = group["vliveSubscribedChannels"]
        channel = list(
            filter(
                lambda x: x["channel_id"] == itx.channel.id and x["group"] == group["id"],
                channels,
            )
        )
        if channel:
            _, status = await Api.vlive_subscribed_channels(channel[0]["id"], "delete")
            message = Embed(
                title="VLIVE subscription removed",
                description=f'This channel has been unsubscribed from VLIVE updates from {group["name"]}',
                color=Color.green(),
            )
        else:
            message = Embed(
                title="VLIVE subscription error",
                description=f'This channel is not subscribed to VLIVE updates from {group["name"]}',
                color=Color.red(),
            )
        await itx.response.send_message(embed=message)


vlive = Vlive()
