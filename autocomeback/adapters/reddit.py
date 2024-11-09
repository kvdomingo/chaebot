import re
from datetime import date, datetime, time
from typing import Any

from bs4 import BeautifulSoup
from loguru import logger
from sqlalchemy import (
    delete,
    func as f,
    select,
)

from autocomeback.adapters.base import BaseAdapter
from autocomeback.config import settings
from autocomeback.db import get_db_context
from autocomeback.models import Comeback
from autocomeback.reddit import get_reddit_client
from autocomeback.schemas import Comeback as ComebackSchema

LISTING_TITLE_PATTERN = re.compile(r"^\w+\s+2\d{3}$")

NUMBER_FROM_ORDINAL_PATTERN = re.compile(r"\d{1,2}")

TODAY = datetime.now().date()

DEFAULT_TZ = settings.DEFAULT_TZ


class RedditAdapter(BaseAdapter):
    async def get_listings(self):
        logger.info("Retrieving listing URLs...")
        listings = []
        async with await get_reddit_client() as cli:
            sub = await cli.subreddit("kpop")
            upcoming = await sub.wiki.get_page("upcoming-releases/archive")

        soup = BeautifulSoup(upcoming.content_html, "lxml")
        toc_children = soup.find_all(attrs={"class": "toc_child"})
        titles: list[str] = [
            li.text.strip()
            for toc_child in toc_children
            for li in toc_child.find_all("li")
        ]

        def loop(parsed_date: date):
            if parsed_date.year >= TODAY.year and parsed_date.month >= TODAY.month:
                return f"{parsed_date.year}/{parsed_date.strftime('%B').lower()}"
            return None

        for title in titles:
            matches = re.match(LISTING_TITLE_PATTERN, title)
            if not matches:
                continue

            parsed_date = datetime.strptime(title, "%B %Y").date()
            listings.append(loop(parsed_date))
            if len(listings) == 1:
                parsed_date = datetime.strptime(title, "%B %Y").date()
                next_month_date = parsed_date.replace(month=parsed_date.month + 1)
                listings.insert(0, loop(next_month_date))

        return [listing for listing in listings if listing is not None]

    async def get_data(self, url: str):
        logger.info(f"Retrieving URL upcoming-releases/{url}...")
        async with await get_reddit_client() as cli:
            sub = await cli.subreddit("kpop")
            releases = await sub.wiki.get_page(f"upcoming-releases/{url}")

        dt_date = datetime.strptime(url, "%Y/%B")

        logger.info("Processing page source...")
        soup = BeautifulSoup(releases.content_html, "lxml")
        table = soup.find("table")
        thead = table.find("thead")
        head_row = thead.find_all("th")
        headers = [header.text.strip().lower().replace(" ", "_") for header in head_row]

        tbody = table.find("tbody")
        rows = tbody.find_all("tr")
        data = []
        for row in rows:
            cells = [td.text.strip() for td in row.find_all("td")]
            row_dict = dict(zip(headers, cells, strict=False))
            row_dict["year"] = dt_date.year
            row_dict["month"] = dt_date.month
            data.append(row_dict)

        logger.info("Extracted data.")
        return data

    @staticmethod
    async def sync_data(data: list[dict[str, Any]]):  # noqa: C901
        logger.info("Validating data...")
        comebacks = []
        last_encountered_day = 1
        for cb in data:
            if cb["album_title"] == "":
                continue

            if cb["day"]:
                match = re.match(NUMBER_FROM_ORDINAL_PATTERN, cb["day"])
                if match:
                    last_encountered_day = int(match.group())

            if cb["time"] and cb["time"] != "?":
                dt_time = datetime.strptime(cb["time"], "%H:%M").time()
            else:
                if "japan" in cb["album_type"].lower():
                    dt_time = time(0, 0, 0)
                else:
                    dt_time = time(18, 0, 0)

            cb["date"] = datetime(
                cb["year"],
                cb["month"],
                last_encountered_day,
                dt_time.hour,
                dt_time.minute,
                0,
                tzinfo=DEFAULT_TZ,
            )
            for key in ["day", "time", "streaming", "year", "month"]:
                if key in cb.keys():
                    cb.pop(key)

            if cb["date"] < datetime.now(DEFAULT_TZ):
                continue

            for key in cb.keys():
                if cb[key] == "":
                    cb[key] = None
            comebacks.append(ComebackSchema(**cb))

        logger.info("Syncing data...")
        status_result = {"processed": 0, "created": 0, "updated": 0, "deleted": 0}

        async with get_db_context() as db:
            for comeback in comebacks:
                existing = (
                    await db.scalars(
                        select(Comeback).where(
                            (Comeback.artist == comeback.artist)
                            & (Comeback.date == comeback.date)
                        )
                    )
                ).first()

                if existing is None:
                    cb = Comeback(
                        **comeback.model_dump(exclude={"id"}), id=str(comeback.id)
                    )
                    db.add(cb)
                    await db.commit()
                    status_result["created"] += 1
                    status_result["processed"] += 1
                else:
                    cb = comeback.model_dump()
                    cb.pop("id")
                    cb.pop("artist")
                    cb.pop("date")
                    [setattr(existing, k, v) for k, v in cb.items()]
                    await db.commit()
                    status_result["updated"] += 1

            logger.info("Purging stale data...")
            dels = (
                await db.scalars(
                    delete(Comeback)
                    .where(Comeback.date < f.now())
                    .returning(Comeback.id)
                )
            ).all()
            await db.commit()
            status_result["deleted"] += len(dels)

        return status_result
