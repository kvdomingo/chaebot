import os
import re
import io
import json
import random
import aiohttp
import asyncio
import twitter
import discord
from dotenv import load_dotenv
from asgiref.sync import sync_to_async
from backend.models import *


load_dotenv()

api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_SECRET'],
)


@sync_to_async
def alias_matcher(member, group, hourly):
    group = Group.objects.get(name=group)
    members = group.members.all().order_by('-id')
    if hourly or member is None or len(member) == 0:
        member = random.choice(members)
        accounts = member.twitter_accounts.all()
        return accounts
    member = ' '.join(member)
    for key in members:
        if (
            re.search(member, key.stage_name, re.I) or
            re.search(key.stage_name, member, re.I) or
            re.search(member, key.given_name, re.I) or
            re.search(key.given_name, member, re.I) or
            re.search(member, key.family_name, re.I) or
            re.search(key.family_name, member, re.I)
        ):
            print(f'Query matched: {str(key)}')
            return key.twitter_accounts.all()
        for alias in key.aliases.all():
            if re.search(alias.alias, member, re.I) or re.search(member, alias.alias, re.I):
                print(f'Query matched: {str(key)}')
                return key.twitter_accounts.all()
    member = random.choice(members)
    accounts = member.twitter_accounts.all()
    print('No match, choosing random')
    return accounts


async def media_handler(group, member=None, hourly=False):
    account_cat = await alias_matcher(member, group, hourly)
    screen_name = random.choice(account_cat).account_name
    tl = api.GetUserTimeline(screen_name=screen_name)
    media_post = (random.choice(tl)).media
    while media_post == None or len(media_post) == 0:
        media_post = random.choice(tl).media
    video_info = media_post[0].video_info
    if video_info is not None:
        for i, vid in enumerate(video_info['variants']):
            if '.m3u8' not in vid['url']:
                link = vid['url']
                async with aiohttp.ClientSession() as session:
                    async with session.get(link) as res:
                        if res.status != 200:
                            return
                        data = io.BytesIO(await res.read())
                        file = discord.File(data, 'video_0.mp4')
                        return [file]
    else:
        links = [media.media_url_https for media in media_post]
        files = []
        async with aiohttp.ClientSession() as session:
            for i, link in enumerate(links):
                async with session.get(link) as res:
                    if res.status != 200:
                        return
                    data = io.BytesIO(await res.read())
                    files.append(discord.File(data, f'image_{i}.jpg'))
            return files


async def bombard_hearts(message):
    reactions = [
        '♥', '💘', '💖', '💗', '💓',
        '💙', '💚', '💛', '💜', '🧡',
        '💝', '💞', '💟', '🖤', '❤',
        '❣', '🤎', '🤍', '😍', '🥰',
    ]
    for react in reactions:
        await message.add_reaction(react)
        await asyncio.sleep(0.5)
