import asyncio
import discord
from typing import List, Tuple, Union


def escape_quote(queries: Union[List[str], Tuple[str]]) -> List[str]:
    return [f"""{query.replace('"', "").replace("'", "").replace("’", "")}""" for query in queries]


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
