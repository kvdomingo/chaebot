from random import SystemRandom

from discord import Color, Embed, Interaction
from discord.app_commands import choices, command, describe
from django.conf import settings
from django.core.cache import cache

from ..handlers.hourly import hourly_handler
from ..utils import escape_quote, get_group_choices

random = SystemRandom()


async def arange(count):
    for i in range(count):
        yield i


@command(description="Get a random pic of the specified member from the specified group")
@describe(group="Name or alias for a group")
@choices(group=get_group_choices())
@describe(person="Name or alias for a group member/idol")
async def query(itx: Interaction, group: str, person: str = ""):
    person = escape_quote([person])
    response, _ = await hourly_handler(group, person)
    timeout = 0
    while not len(response):
        if timeout == 5:
            return
        response, _ = await hourly_handler(group, person)
        timeout += 1

    if isinstance(response, list):
        await itx.response.send_message(files=response)
    elif isinstance(response, str):
        await itx.response.send_message(response)


@command(description="Spam the channel with media of a group member/idol (maximum of 10)")
@describe(number="Number of media to spam")
@describe(group="Name or alias for a group")
@choices(group=get_group_choices())
@describe(person="Name or alias for a group member/idol")
async def spam(itx: Interaction, number: int, group: str, person: str):
    if itx.message.author.id != settings.DISCORD_ADMIN_ID:
        number = min([number, 10])
    person = escape_quote([person])
    sent = 0
    async for _ in arange(number):
        do = lambda: hourly_handler(group, person)
        response, _ = await do()
        while not response:
            response, _ = await do()
        await itx.response.send_message(files=response)
        sent += len(response)
        if sent >= number:
            break


@command(name="list")
async def list_(itx: Interaction):
    supp_groups = []
    for group in cache.get("groups"):
        without_source = [len(member["twitterMediaSources"]) == 0 for member in group["members"]]
        if any(without_source):
            continue
        supp_groups.append(group["name"])
    embed = Embed(
        title="Groups/artists in database:",
        description="\n".join(supp_groups),
        color=Color.green(),
    )
    await itx.response.send_message(embed=embed)
