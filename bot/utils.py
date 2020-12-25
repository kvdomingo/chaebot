import discord
from typing import List, Tuple, Union, Dict
from src.handlers.twitter import twitter_handler as twitter_handler


def escape_quote(queries: Union[List[str], Tuple[str]]) -> List[str]:
    return [f"""{query.replace('"', "").replace("'", "").replace("’", "")}""" for query in queries]


def query_string_from_dict(query_dict: Dict):
    return '&'.join([f'{k}={v}' for k, v in query_dict.items()])


async def query_handler(ctx, group: str, person: Union[List[str], Tuple[str]]):
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
