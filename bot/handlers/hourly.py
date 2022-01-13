import aiohttp
import discord
import io
import os
import re
import twitter
from django.core.cache import cache
from random import SystemRandom
from typing import List, Tuple


random = SystemRandom()
api = twitter.Api(
    consumer_key=os.environ.get("TWITTER_CONSUMER_KEY"),
    consumer_secret=os.environ.get("TWITTER_CONSUMER_SECRET"),
    access_token_key=os.environ.get("TWITTER_ACCESS_KEY"),
    access_token_secret=os.environ.get("TWITTER_ACCESS_SECRET"),
)


async def group_name_matcher(name: str, random_on_no_match: bool = True) -> dict:
    groups = cache.get("groups")
    group_names = {}
    for group in groups:
        group_names[group["id"]] = [group["name"]]
        for alias in group["aliases"]:
            group_names[group["id"]].append(alias["alias"])
    for id_, aliases in group_names.items():
        search_params = []
        for alias in aliases:
            search_params.extend(
                [
                    re.search(name, alias, re.I),
                    re.search(alias, name, re.I),
                ]
            )
            if any(search_params):
                group = list(filter(lambda x: x["id"] == id_, groups))[0]
                print(f'Group query matched: {group["name"]}')
                return group
    if random_on_no_match:
        print("No group query matched, choosing random")
        return random.choice(groups)
    else:
        return {}


async def member_name_matcher(
    _member: List[str], group: str, hourly: bool
) -> Tuple[list, dict]:
    group = await group_name_matcher(group)
    members = group["members"]
    if hourly or not _member:
        member = random.choice(members)
        accounts = member["twitterMediaSources"]
        return accounts, group
    _member = " ".join(_member)
    for key in members:
        search_parameters = [
            re.search(_member, key["stage_name"], re.I),
            re.search(key["stage_name"], _member, re.I),
            re.search(_member, key["given_name"], re.I),
            re.search(key["given_name"], _member, re.I),
            re.search(_member, key["family_name"], re.I),
            re.search(key["family_name"], _member, re.I),
        ]
        if key["english_name"]:
            search_parameters.extend(
                [
                    re.search(key["english_name"], _member),
                    re.search(_member, key["english_name"]),
                ]
            )
        if any(search_parameters):
            print(f'Member query matched: {key["stage_name"]} of {group["name"]}')
            return key["twitterMediaSources"], group
        for alias in key["aliases"]:
            if re.search(alias["alias"], _member, re.I) or re.search(
                _member, alias["alias"], re.I
            ):
                print(f'Member query matched: {key["stage_name"]} of {group["name"]}')
                return key["twitterMediaSources"], group
    print("No member query matched, choosing random")
    accounts = random.choice(members)["twitterMediaSources"]
    return accounts, group


async def hourly_handler(
    group: str,
    member: List[str] = None,
    hourly: bool = False,
    spam_number: int = 1,
    max_retries: int = 10,
) -> Tuple[list, dict]:
    account_cat, group = await member_name_matcher(member, group, hourly)
    screen_name = random.choice(account_cat)["account_name"]
    spam_number = min(spam_number, 50)

    if spam_number <= 25:
        tl_count = 50
    else:
        tl_count = 100

    try:
        tl = api.GetUserTimeline(
            screen_name=screen_name,
            exclude_replies=True,
            include_rts=False,
            count=tl_count,
        )
    except twitter.error.TwitterError:
        return [], {}

    if not tl:
        for _ in range(max_retries):
            try:
                tl = api.GetUserTimeline(
                    screen_name=screen_name,
                    exclude_replies=True,
                    include_rts=False,
                    count=tl_count,
                )
            except twitter.error.TwitterError:
                continue
            if tl:
                break

    if not tl:
        return [], {}

    files = []
    while len(files) < spam_number:
        media_post = (random.choice(tl)).media
        if media_post is None or len(media_post) == 0:
            for _ in range(max_retries):
                media_post = (random.choice(tl)).media
                if media_post:
                    break
        video_info = media_post[0].video_info
        if video_info is not None:
            variants = video_info["variants"]
            bitrates = []
            for variant in variants:
                if "bitrate" in variant.keys():
                    bitrates.append(variant["bitrate"])
                else:
                    bitrates.append(0)
            max_bitrate_loc = bitrates.index(max(bitrates))
            vid = variants[max_bitrate_loc]
            link = vid["url"]
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as res:
                    if res.status != 200:
                        continue
                    data = io.BytesIO(await res.read())
                    file = discord.File(data, f"video_{len(files)}.mp4")
                    files.append(file)
        else:
            links = [media.media_url_https for media in media_post]
            async with aiohttp.ClientSession() as session:
                for i, link in enumerate(links):
                    async with session.get(link) as res:
                        if res.status != 200:
                            continue
                        data = io.BytesIO(await res.read())
                        files.append(discord.File(data, f"image_{len(files)}.jpg"))
    return files, group
