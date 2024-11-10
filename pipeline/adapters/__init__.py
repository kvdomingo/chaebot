from pipeline.adapters.base import BaseAdapter
from pipeline.adapters.dbkpop import DbKpopAdapter
from pipeline.adapters.reddit import RedditAdapter

adapters: dict[str, BaseAdapter] = {
    "DBKPOP": DbKpopAdapter(),
    "REDDIT": RedditAdapter(),
}


__all__ = ["adapters"]
