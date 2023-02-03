import io
import re
from random import SystemRandom

import aiohttp
import discord
import twitter
from django.conf import settings

from bot.api.internal import Api
from kvisualbot.logging import logger

random = SystemRandom()

api = twitter.Api(
    consumer_key=settings.TWITTER_CONSUMER_KEY,
    consumer_secret=settings.TWITTER_CONSUMER_SECRET,
    access_token_key=settings.TWITTER_ACCESS_KEY,
    access_token_secret=settings.TWITTER_ACCESS_SECRET,
)


async def group_name_matcher(name: str, random_on_no_match: bool = True) -> dict:
    groups = Api.sync_groups()
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
                logger.info(f'Group query matched: {group["name"]}')
                return group
    if random_on_no_match:
        logger.info("No group query matched, choosing random")
        return random.choice(groups)
    else:
        return {}


async def member_name_matcher(_member: list[str], group: str, hourly: bool) -> tuple[list, dict]:
    if len(_member) == 1 and not _member[0]:
        _member = None
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
            logger.info(f'Member query matched: {key["stage_name"]} of {group["name"]}')
            return key["twitterMediaSources"], group
        for alias in key["aliases"]:
            if re.search(alias["alias"], _member, re.I) or re.search(_member, alias["alias"], re.I):
                logger.info(f'Member query matched: {key["stage_name"]} of {group["name"]}')
                return key["twitterMediaSources"], group
    logger.info("No member query matched, choosing random")
    accounts = random.choice(members)["twitterMediaSources"]
    return accounts, group


async def hourly_handler(
    group_: str, member: list[str] = None, hourly: bool = False, max_retries: int = 10
) -> tuple[list, dict]:
    account_cat, group = await member_name_matcher(member, group_, hourly)
    retries = 0
    while len(account_cat) == 0:
        account_cat, group = await member_name_matcher(member, group_, hourly)
        retries += 1
        if retries == max_retries:
            return [], {}
    screen_name = random.choice(account_cat)["account_name"]
    tl_count = 50

    try:
        tl = api.GetUserTimeline(
            screen_name=screen_name,
            exclude_replies=True,
            include_rts=False,
            count=tl_count,
        )
    except twitter.error.TwitterError as e:
        logger.error(str(e))
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
    while len(files) < 1:
        media_post = (random.choice(tl)).media
        if media_post is None or len(media_post) == 0:
            for _ in range(max_retries):
                media_post = (random.choice(tl)).media
                if media_post and len(media_post) > 0:
                    break

        async with aiohttp.ClientSession() as session:
            match type_ := media_post[0].type:
                case "video" | "animated_gif":
                    video_info = media_post[0].video_info
                    variants = video_info["variants"]
                    if type_ == "video":
                        bitrates = [variant.get("bit_rate") or 0 for variant in variants]
                        max_bitrate_loc = bitrates.index(max(bitrates))
                        vid = variants[max_bitrate_loc]
                        link = vid["url"]
                        prefix = "video"
                    else:
                        link = variants[0]["url"]
                        prefix = "gif"
                    async with session.get(link) as res:
                        if not res.ok:
                            continue
                        buffer = io.BytesIO(await res.read())
                        buffer.seek(0)
                        file = discord.File(buffer, f"{prefix}_{len(files)}.mp4")
                        files.append(file)
                case "photo":
                    links = [media.media_url_https for media in media_post]
                    for i, link in enumerate(links):
                        async with session.get(link) as res:
                            if not res.ok:
                                continue
                            buffer = io.BytesIO(await res.read())
                            buffer.seek(0)
                            files.append(discord.File(buffer, f"image_{len(files)}.jpg"))
                case _:
                    return [], {}
    return files, group
