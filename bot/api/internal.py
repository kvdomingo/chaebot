import aiohttp
import requests
from aiohttp import ClientResponse
from django.conf import settings
from loguru import logger

BASE_URL = f"{settings.API_HOST}/api"


async def _arequest(endpoint: str, method: str = "get", body: dict = None):
    async with aiohttp.ClientSession() as session:
        api = getattr(session, method)
        async with api(f"{BASE_URL}/{endpoint}", json=body) as res:
            res: ClientResponse
            logger.debug(f"{res.request_info.method} {res.request_info.url}")
            logger.debug(await res.text())
            return res


class Api:
    @staticmethod
    def sync_groups() -> dict:
        with requests.Session() as session:
            with session.get(f"{BASE_URL}/groups") as res:
                return res.json()

    @staticmethod
    async def groups():
        return await _arequest("groups")

    @staticmethod
    async def group(group_id, method="get", body=None):
        return await _arequest(f"group/{group_id}", method, body)

    @staticmethod
    async def group_aliases(group_id: int):
        return await _arequest(f"group/{group_id}/aliases")

    @staticmethod
    async def group_members(group_id: int):
        return await _arequest(f"group/{group_id}/members")

    @staticmethod
    async def group_twitter_media_subscribed_channels(group_id: int):
        return await _arequest(f"group/{group_id}/twitterMediaSubscribedChannels")

    @staticmethod
    async def members():
        return await _arequest("members")

    @staticmethod
    async def member(member_id, method="get", body=None):
        return await _arequest(f"member/{member_id}", method, body)

    @staticmethod
    async def member_aliases(member_id: int):
        return await _arequest(f"member/{member_id}/aliases")

    @staticmethod
    async def member_twitter_media_sources(member_id: int):
        return await _arequest(f"member/{member_id}/twitterMediaSources")

    @staticmethod
    async def twitter_media_subscribed_channels(pk=None, method="get", body=None):
        if pk is None:
            return await _arequest("twitterMediaSubscribedChannels", method, body)
        return await _arequest(f"twitterMediaSubscribedChannel/{pk}", method, body)

    @staticmethod
    async def schedule_subscribers(pk=None, method="get", body=None):
        if pk is None:
            return await _arequest("scheduleSubscribers", method, body)
        return await _arequest(f"scheduleSubscribers/{pk}", method, body)

    @staticmethod
    async def schedule_subscriber_from_guild(guild_id: int):
        return await _arequest(f"scheduleSubscriberFromGuild/{guild_id}", "get", None)

    @staticmethod
    async def emote_cache(pk=None, method="get", body=None):
        if pk is None:
            return await _arequest("emoteCache", method, body)
        return await _arequest(f"emoteCache/{pk}", method, body)

    @staticmethod
    async def emote_usage(pk=None, method="get", body=None):
        if pk is None:
            return await _arequest("emoteUsage", method, body)
        return await _arequest(f"emoteUsage/{pk}", method, body)

    @staticmethod
    async def sticker_cache(pk=None, method="get", body=None):
        if pk is None:
            return await _arequest("stickerCache", method, body)
        return await _arequest(f"stickerCache/{pk}", method, body)

    @staticmethod
    async def sticker_usage(pk=None, method="get", body=None):
        if pk is None:
            return await _arequest("stickerUsage", method, body)
        return await _arequest(f"stickerUsage/{pk}", method, body)

    @staticmethod
    async def user_cache(pk=None, method="get", body=None):
        if pk is None:
            return await _arequest("userCache", method, body)
        return await _arequest(f"userCache/{pk}", method, body)
