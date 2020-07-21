import asyncio
import discord
from typing import List, Tuple, Union
from src.handlers.twitter import media_handler as twitter_handler


def escape_quote(queries: Union[List[str], Tuple[str]]) -> List[str]:
    return [f"""{query.replace('"', "").replace("'", "").replace("’", "")}""" for query in queries]


async def query_handler(ctx, group: str, person: Union[List[str], Tuple[str]]):
    person = escape_quote(person)
    media = await twitter_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


async def bombard_hearts(message: discord.Message):
    reactions = [
        '♥', '💘', '💖', '💗', '💓',
        '💙', '💚', '💛', '💜', '🧡',
        '💝', '💞', '💟', '🖤', '❤',
        '❣', '🤎', '🤍', '😍', '🥰',
    ]
    for react in reactions:
        await message.add_reaction(react)
        await asyncio.sleep(0.5)
