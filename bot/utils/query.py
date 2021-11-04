import discord
from . import escape_quote
from ..handlers.hourly import hourly_handler


def query_string_from_dict(query_dict: dict) -> str:
    return '&'.join([f'{k}={v}' for k, v in query_dict.items()])


async def query_handler(ctx, group: str, person: list[str]) -> None:
    person = escape_quote(person)
    response = await hourly_handler(group, person)
    while not len(response):
        response = await hourly_handler(group, person)

    if isinstance(response, list):
        message = await ctx.send(files=response)
        await bombard_hearts(message)
    elif isinstance(response, str):
        await ctx.send(response)


async def bombard_hearts(message: discord.Message) -> None:
    pass
    # TODO: Implement opt-in/opt-out system for individual servers
    # import asyncio
    # reactions = [
    #     '♥', '💘', '💖', '💗', '💓',
    #     '💙', '💚', '💛', '💜', '🧡',
    #     '💝', '💞', '💟', '🖤', '❤',
    #     '❣', '🤎', '🤍', '😍', '🥰',
    # ]
    # for react in reactions:
    #     await message.add_reaction(react)
    #     await asyncio.sleep(0.5)
