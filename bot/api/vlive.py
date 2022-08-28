from typing import Awaitable, Union

import aiohttp

BASE_URL = "https://www.vlive.tv"


async def _arequest(
    endpoint: str, method: str = "get", body: dict = None, params: dict = None
) -> Awaitable[Union[dict, list]]:
    async with aiohttp.ClientSession() as session:
        api = getattr(session, method)
        url = f"{BASE_URL}/{endpoint}"
        if len(params.keys()) > 0:
            url = f"{url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        async with api(url, data=body) as res:
            return await res.json()


def search_channels(search: str) -> Awaitable[Union[dict, list]]:
    return _arequest(
        "search/auto/channels",
        params={
            "dataType": "json",
            "query": search,
            "maxNumOfRows": 5,
        },
    )
