import discord
from typing import Iterable
from . import escape_quote
from ..handlers.twitter import twitter_handler


async def query_handler(ctx, group: str, person: Iterable[str]):
    person = escape_quote(person)
    response = await twitter_handler(group, person)
    while not len(response):
        response = await twitter_handler(group, person)

    if isinstance(response, list):
        message = await ctx.send(files=response)
        await bombard_hearts(message)
    elif isinstance(response, str):
        await ctx.send(response)


async def bombard_hearts(message: discord.Message):
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
