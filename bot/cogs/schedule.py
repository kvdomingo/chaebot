import asyncio
import random
from datetime import datetime, time, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from discord import Client, TextChannel
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context
from django.conf import settings
from loguru import logger

from bot.api.internal import Api
from bot.firestore import get_firestore_client
from bot.utils import SeverityLevel, generate_embed


class Schedule(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.update_schedule.start()

    def cog_unload(self):
        self.update_schedule.cancel()

    @commands.group(hidden=True)
    async def schedule(self, ctx: Context):
        pass

    @schedule.command(aliases=["sub"], help="Subscribe to upcoming comebacks calendar")
    async def subscribe(self, ctx: Context, channel: TextChannel):
        subscriber, status = await Api.schedule_subscribers(
            method="post",
            body={"guild_id": ctx.guild.id, "channel_id": channel.id, "message_id": None},
        )
        if status != HTTPStatus.CREATED:
            embed = generate_embed(
                title="Adding schedule subscription failed",
                content="due to the following error(s):",
                severity=SeverityLevel.ERROR,
                footer="Please check the errors above or try again later.",
                fields=subscriber,
            )
            await ctx.send(embed=embed)
            return

        schedule = await self.get_schedule()
        schedule_strings = self.to_schedule_strings(schedule)
        embed = generate_embed(
            title="Upcoming comebacks",
            severity=SeverityLevel.INFO,
            content=schedule_strings,
            footer="KST (UTC+9) | Shows the next 30 days of events",
        )
        channel = ctx.guild.get_channel(channel.id)
        msg = await channel.send(embed=embed)
        res, status = await Api.schedule_subscribers(subscriber["id"], "patch", {"message_id": msg.id})
        if status != 200:
            embed = generate_embed(
                title="Adding schedule subscription failed",
                content="due to the following error(s):",
                severity=SeverityLevel.ERROR,
                footer="Please check the errors above or try again later.",
                fields=res,
            )
            await msg.delete()
            await ctx.send(embed=embed)
            return

        embed = generate_embed(
            title="Adding schedule subscription success",
            content=f"The channel {channel.mention} has been subscribed to upcoming comebacks schedule.",
            severity=SeverityLevel.SUCCESS,
        )
        return await ctx.send(embed=embed)

    @schedule.command(aliases=["unsub"], help="Unsubscribe to upcoming comebacks calendar")
    async def unsubscribe(self, ctx: Context, channel: TextChannel):
        res = await Api.schedule_subscriber_from_guild(ctx.guild.id)
        channel = self.client.get_channel(channel.id)
        msg = channel.get_partial_message(res["message_id"])
        await msg.delete()
        await Api.schedule_subscribers(res["id"], "delete")
        embed = generate_embed(
            title="Unsubscribing to comeback schedule success",
            content=f"The channel {channel.mention} has been unsubscribed from upcoming comebacks schedule.",
            severity=SeverityLevel.SUCCESS,
        )
        await ctx.send(embed=embed)

    @schedule.command(help="Manually invoke schedule update", hidden=True)
    async def update(self, ctx: Context):
        logger.info("Manual schedule update invoked.")
        msg = await ctx.send("Updating schedule...")
        await self.update_schedule()
        await msg.delete()

    @staticmethod
    async def get_schedule():
        logger.info("Fetching comeback schedule...")
        db = get_firestore_client()
        coll_ref = (
            db.collection("cb-reddit")
            .order_by("date")
            .where("date", "<", datetime.now(ZoneInfo(settings.TIME_ZONE)) + timedelta(days=30))
        )
        return [doc.to_dict() async for doc in coll_ref.stream()]

    @staticmethod
    def to_schedule_strings(schedule: list[dict]) -> list[str]:
        logger.info("Formatting schedule strings...")
        if len(schedule) == 0:
            return ["None"]
        cb_strings = []
        for doc in schedule:
            dt: datetime = doc["date"].astimezone(ZoneInfo(settings.TIME_ZONE))
            dt_date = dt.strftime("%b %d")
            dt_time = dt.strftime("%H:%M")
            is_today = "`<today>`" if dt.date() == datetime.now(ZoneInfo(settings.TIME_ZONE)).date() else ""
            if (descriptor := doc.get("album_type")) is not None:
                descriptor = descriptor.title()
            else:
                if (descriptor := doc.get("release")) is not None:
                    if "japan" in descriptor.lower():
                        descriptor = "Japan"
                    else:
                        descriptor = descriptor.title()
                else:
                    descriptor = ""
            cb_strings.append(
                f"`[{dt_date} | {dt_time}]` **{doc['artist']}** {descriptor} 『{doc['album_title']}』 {is_today}"
            )
        return cb_strings

    @tasks.loop(time=[time(h, 0, 0, tzinfo=ZoneInfo(settings.TIME_ZONE)) for h in [0, 6, 12, 18]])
    async def update_schedule(self):
        schedule = await self.get_schedule()
        schedule_strings = self.to_schedule_strings(schedule)
        logger.info("Updating comeback schedule...")
        subscribers = await Api.schedule_subscribers()
        for sub in subscribers:
            guild = self.client.get_guild(sub["guild_id"])
            channel = guild.get_channel(sub["channel_id"])
            msg = channel.get_partial_message(sub["message_id"])
            embed = generate_embed(
                title="Upcoming comebacks",
                severity=SeverityLevel.INFO,
                content=schedule_strings,
                footer="KST (UTC+9) | Shows the next 30 days of events",
            )
            await msg.edit(embed=embed)

    @update_schedule.before_loop
    async def before_update_schedule(self):
        # wait between 5-10 minutes
        await asyncio.sleep(random.randrange(5 * 60, 10 * 60))


async def setup(client: Bot):
    await client.add_cog(Schedule(client))
