import aiohttp
import discord
import io
import os
import re
import twitter
from random import SystemRandom
from src import Session
from src.models import *
from typing import List, Union


random = SystemRandom()
api = twitter.Api(
    consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
    consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
    access_token_key=os.environ.get('TWITTER_ACCESS_KEY'),
    access_token_secret=os.environ.get('TWITTER_ACCESS_SECRET'),
)


async def alias_matcher(member: List[str], group: str, hourly: bool) -> List[TwitterAccount]:
    sess = Session()
    members = sess.query(Member).filter(Member.group.has(name=group)).order_by(Member.id.desc()).all()
    if hourly or not member:
        member = random.choice(members)
        accounts = member.twitter_accounts
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
            return key.twitter_accounts
        for alias in key.aliases:
            if re.search(alias.alias, member, re.I) or re.search(member, alias.alias, re.I):
                print(f'Query matched: {str(key)}')
                return key.twitter_accounts
    member = random.choice(members)
    accounts = member.twitter_accounts
    print('No match, choosing random')
    sess.close()
    return accounts


async def media_handler(
        group: str,
        member: List[str] = None,
        hourly: bool = False
) -> Union[list, str]:
    account_cat = await alias_matcher(member, group, hourly)
    screen_name = random.choice(account_cat).account_name
    try:
        tl = api.GetUserTimeline(
            screen_name=screen_name,
            exclude_replies=True,
            include_rts=False,
            count=100,
        )
    except twitter.error.TwitterError:
        return []
    media_post = (random.choice(tl)).media
    while media_post is None or len(media_post) == 0:
        media_post = random.choice(tl).media
    video_info = media_post[0].video_info
    if video_info is not None:
        variants = video_info['variants']
        bitrates = []
        for variant in variants:
            if 'bitrate' in variant.keys():
                bitrates.append(variant['bitrate'])
            else:
                bitrates.append(0)
        max_bitrate_loc = bitrates.index(max(bitrates))
        vid = variants[max_bitrate_loc]
        link = vid['url']
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as res:
                if res.status != 200:
                    message = "Sorry, I'm having some trouble talking to Twitter :upside_down: Try that again in a few seconds"
                    return message
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
                        message = "Sorry, I'm having some trouble talking to Twitter :upside_down: Try that again in a few seconds"
                        return message
                    data = io.BytesIO(await res.read())
                    files.append(discord.File(data, f'image_{i}.jpg'))
            return files
