from abc import ABC, abstractmethod
from itertools import chain


class BaseAdapter(ABC):
    @abstractmethod
    async def get_listings(self):
        pass

    @abstractmethod
    async def get_data(self, url):
        pass

    @staticmethod
    @abstractmethod
    async def sync_data(data):
        pass

    async def __call__(self):
        listings = await self.get_listings()
        data = list(chain(*[await self.get_data(listing) for listing in listings]))
        result = await self.sync_data(data)
        return result
