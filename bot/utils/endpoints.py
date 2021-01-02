import aiohttp
from django.conf import settings

# if settings.PYTHON_ENV == 'development':
#     BASE_URL = 'http://localhost:8000'
# else:
BASE_URL = 'https://kvisualbot-django.herokuapp.com'

BASE_URL += '/v1.0'


async def _arequest(endpoint: str, params: dict = None):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{BASE_URL}/{endpoint}', params=params) as res:
            return await res.json()


class Api:
    @staticmethod
    async def groups():
        return await _arequest('groups')

    @staticmethod
    async def group(group_id):
        return await _arequest(f'group/{group_id}')

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
    async def member(member_id):
        return await _arequest(f'member/{member_id}')

    @staticmethod
    async def member_aliases(member_id: int):
        return await _arequest(f'member/{member_id}/aliases')

    @staticmethod
    async def member_twitter_media_sources(member_id: int):
        return await _arequest(f'member/{member_id}/twitterMediaSources')
