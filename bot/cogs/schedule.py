import asyncio
import random
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from discord import Client, TextChannel
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context
from loguru import logger
from sqlalchemy import select

from bot.utils import SeverityLevel, generate_embed, generate_schedule_fields
from common.db import get_db_context
from common.models import ScheduleSubscriber
from common.schemas import ScheduleSubscriber as ScheduleSubscriberSchema
from common.settings import settings


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
        async with get_db_context() as db:
            try:
                subscriber = ScheduleSubscriberSchema(
                    guild_id=ctx.guild.id, channel_id=channel.id
                )
                db.add(subscriber)
                await db.commit()
            except Exception as e:
                logger.error(e)
                embed = generate_embed(
                    title="Adding schedule subscription failed",
                    content="due to errors.",
                    severity=SeverityLevel.ERROR,
                    footer="Please try again later.",
                )
                await ctx.send(embed=embed)
                return

            schedule = await self.get_schedule()
            schedule_strings = generate_schedule_fields(schedule)
            embed = generate_embed(
                title="Upcoming comebacks",
                severity=SeverityLevel.INFO,
                fields=schedule_strings,
                footer="KST (UTC+9) | Shows the next 30 days of events",
            )
            channel = ctx.guild.get_channel(channel.id)
            msg = await channel.send(embed=embed)

            res = await db.scalar(
                select(ScheduleSubscriber).where(ScheduleSubscriber.id == subscriber.id)
            )

            try:
                res.message_id = msg.id
                res.save()
                await db.commit()
            except Exception as e:
                logger.error(e)
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

    @schedule.command(
        aliases=["unsub"], help="Unsubscribe to upcoming comebacks calendar"
    )
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
            .where(
                "date",
                "<",
                datetime.now(ZoneInfo(settings.TIME_ZONE)) + timedelta(days=30),
            )
        )
        return [doc.to_dict() async for doc in coll_ref.stream()]

    @tasks.loop(
        time=[
            time(h, 0, 0, tzinfo=ZoneInfo(settings.TIME_ZONE)) for h in [0, 6, 12, 18]
        ]
    )
    async def update_schedule(self):
        schedule = await self.get_schedule()
        schedule_fields = generate_schedule_fields(schedule)
        logger.info("Updating comeback schedule...")
        subscribers = await Api.schedule_subscribers()
        for sub in subscribers:
            guild = self.client.get_guild(sub["guild_id"])
            channel = guild.get_channel(sub["channel_id"])
            msg = channel.get_partial_message(sub["message_id"])
            embed = generate_embed(
                title="Upcoming comebacks",
                severity=SeverityLevel.INFO,
                fields=schedule_fields,
                footer="KST (UTC+9) | Shows the next 30 days of events",
            )
            await msg.edit(embed=embed)

    @update_schedule.before_loop
    async def before_update_schedule(self):
        # wait between 5-10 minutes
        await asyncio.sleep(random.randrange(5 * 60, 10 * 60))


async def setup(client: Bot):
    await client.add_cog(Schedule(client))
