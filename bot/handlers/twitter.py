import aiohttp
import discord
import io
import os
import re
import twitter
from random import SystemRandom
from asgiref.sync import sync_to_async
from ..models import *
from typing import List, Union


random = SystemRandom()
api = twitter.Api(
    consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
    consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
    access_token_key=os.environ.get('TWITTER_ACCESS_KEY'),
    access_token_secret=os.environ.get('TWITTER_ACCESS_SECRET'),
)


@sync_to_async
def alias_matcher(member: List[str], group: str, hourly: bool) -> List[TwitterMediaSource]:
    members = Member.objects.filter(group__name=group).order_by('-id').all()
    if hourly or not member:
        member = random.choice(members)
        accounts = member.twitter_media_sources
        return accounts
    member = ' '.join(member)
    for key in members:
        search_parameters = [
            re.search(member, key.stage_name, re.I),
            re.search(key.stage_name, member, re.I),
            re.search(member, key.given_name, re.I),
            re.search(key.given_name, member, re.I),
            re.search(member, key.family_name, re.I),
            re.search(key.family_name, member, re.I)
        ]
        if key.english_name:
            search_parameters.extend([
                re.search(key.english_name, member),
                re.search(member, key.english_name),
            ])
        if any(search_parameters):
            print(f'Query matched: {str(key)}')
            return key.twitter_accounts
        for alias in key.aliases:
            if re.search(alias.alias, member, re.I) or re.search(member, alias.alias, re.I):
                print(f'Query matched: {str(key)}')
                return key.twitter_accounts

    member = random.choice(members)
    accounts = member.twitter_media_sources
    print('No match, choosing random')
    return accounts


def twitter_handler(
        group: str,
        member: List[str] = None,
        hourly: bool = False
) -> Union[list, str]:
    account_cat = alias_matcher(member, group, hourly)
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
                    return []
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
                        return []
                    data = io.BytesIO(await res.read())
                    files.append(discord.File(data, f'image_{i}.jpg'))
            return files
