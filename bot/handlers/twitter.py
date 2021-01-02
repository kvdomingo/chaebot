import aiohttp
import discord
import io
import os
import re
import twitter
from ..utils.endpoints import Api
from random import SystemRandom
from typing import List, Union, Tuple


random = SystemRandom()
api = twitter.Api(
    consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
    consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
    access_token_key=os.environ.get('TWITTER_ACCESS_KEY'),
    access_token_secret=os.environ.get('TWITTER_ACCESS_SECRET'),
)


async def group_name_matcher(name: str) -> dict:
    groups = await Api.groups()
    group_names = {}
    for group in groups:
        group_names[group['id']] = [group['name']]
        for alias in group['aliases']:
            group_names[group['id']].append(alias['alias'])
    for id_, aliases in group_names.items():
        search_params = []
        for alias in aliases:
            search_params.extend([
                re.search(name, alias, re.I),
                re.search(alias, name, re.I),
            ])
            if any(search_params):
                return list(filter(lambda x: x['id'] == id_, groups))[0]
    return random.choice(groups)


async def member_name_matcher(member: List[str], group: str, hourly: bool) -> Tuple[list, dict]:
    group = await group_name_matcher(group)
    members = group['members']
    if hourly or not member:
        member = random.choice(members)
        accounts = member['twitterMediaSources']
        return accounts, group
    member = ' '.join(member)
    for key in members:
        search_parameters = [
            re.search(member, key['stage_name'], re.I),
            re.search(key['stage_name'], member, re.I),
            re.search(member, key['given_name'], re.I),
            re.search(key['given_name'], member, re.I),
            re.search(member, key['family_name'], re.I),
            re.search(key['family_name'], member, re.I)
        ]
        if key['english_name']:
            search_parameters.extend([
                re.search(key['english_name'], member),
                re.search(member, key['english_name']),
            ])
        if any(search_parameters):
            print(f'Member query matched: {key["stage_name"]}')
            return key['twitterMediaSources'], group
        for alias in key['aliases']:
            if re.search(alias['alias'], member, re.I) or re.search(member, alias['alias'], re.I):
                print(f'Member query matched: {str(key)}')
                return key['twitterMediaSources'], group
    print('No member query matched, choosing random')
    accounts = random.choice(members)['twitterMediaSources']
    return accounts, group


async def twitter_handler(
        group: str,
        member: List[str] = None,
        hourly: bool = False
) -> Tuple[list, dict]:
    account_cat, group = await member_name_matcher(member, group, hourly)
    screen_name = random.choice(account_cat)['account_name']
    try:
        tl = api.GetUserTimeline(
            screen_name=screen_name,
            exclude_replies=True,
            include_rts=False,
            count=50,
        )
    except twitter.error.TwitterError:
        return [], {}
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
                return [file], group
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
            return files, group
