import aiohttp
import requests
from django.conf import settings

if settings.PYTHON_ENV == 'development':
    BASE_URL = 'http://localhost:8000'
else:
    BASE_URL = 'https://kvisualbot.xyz'

API_VERSION = 'v1.0'

BASE_URL += f'/{API_VERSION}'


async def _arequest(endpoint: str, method: str = 'get', body: dict = None):
    async with aiohttp.ClientSession() as session:
        api = getattr(session, method)
        async with api(f'{BASE_URL}/{endpoint}', data=body) as res:
            if method in ['post', 'patch']:
                return await res.json(), res.status
            if method == 'delete':
                return [], res.status
            return await res.json()


class Api:
    @staticmethod
    def sync_groups():
        with requests.Session() as session:
            with session.get(f'{BASE_URL}/groups') as res:
                return res.json()

    @staticmethod
    async def groups():
        return await _arequest('groups')

    @staticmethod
    async def group(group_id, method='get', body=None):
        return await _arequest(f'group/{group_id}', method, body)

    @staticmethod
    async def group_aliases(group_id: int):
        return await _arequest(f'group/{group_id}/aliases')

    @staticmethod
    async def group_members(group_id: int):
        return await _arequest(f'group/{group_id}/members')

    @staticmethod
    async def group_twitter_media_subscribed_channels(group_id: int):
        return await _arequest(f'group/{group_id}/twitterMediaSubscribedChannels')

    @staticmethod
    async def group_vlive_subscribed_channels(group_id: int):
        return await _arequest(f'group/{group_id}/vliveSubscribedChannels')

    @staticmethod
    async def members():
        return await _arequest('members')

    @staticmethod
    async def member(member_id, method='get', body=None):
        return await _arequest(f'member/{member_id}', method, body)

    @staticmethod
    async def member_aliases(member_id: int):
        return await _arequest(f'member/{member_id}/aliases')

    @staticmethod
    async def member_twitter_media_sources(member_id: int):
        return await _arequest(f'member/{member_id}/twitterMediaSources')

    @staticmethod
    async def twitter_media_subscribed_channels(pk=None, method='get', body=None):
        if pk is None:
            return await _arequest(f'twitterMediaSubscribedChannels', method, body)
        return await _arequest(f'twitterMediaSubscribedChannel/{pk}', method, body)

    @staticmethod
    async def vlive_subscribed_channels(pk=None, method='get', body=None):
        if pk is None:
            return await _arequest(f'vliveSubscribedChannels', method, body)
        return await _arequest(f'vliveSubscribedChannel/{pk}', method, body)
