from autocomeback.adapters.base import BaseAdapter
from autocomeback.adapters.dbkpop import DbKpopAdapter
from autocomeback.adapters.reddit import RedditAdapter

adapters: dict[str, BaseAdapter] = {
    "DBKPOP": DbKpopAdapter(),
    "REDDIT": RedditAdapter(),
}


__all__ = ["adapters"]
