import asyncio
import json
import random
from datetime import time, timedelta

from discord import Client, TextChannel
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context
from loguru import logger
from sqlalchemy import DATE, Interval, cast, delete, func, select

from bot.utils import SeverityLevel, generate_embed, generate_schedule_fields
from common.db import get_db_context
from common.models import Comeback, ScheduleSubscriber
from common.schemas import (
    Comeback as ComebackSchema,
    ScheduleSubscriber as ScheduleSubscriberSchema,
)
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
                db.add(ScheduleSubscriber(**subscriber.model_dump(mode="json")))
                await db.commit()
            except Exception as e:
                logger.error(e)
                embed = generate_embed(
                    title="Adding schedule subscription failed",
                    content="Please try again later.",
                    severity=SeverityLevel.ERROR,
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
                select(ScheduleSubscriber).where(
                    ScheduleSubscriber.id == str(subscriber.id)
                )
            )

            try:
                res.message_id = msg.id
                await db.commit()
            except Exception as e:
                logger.error(e)
                embed = generate_embed(
                    title="Adding schedule subscription failed",
                    content="Please check the errors above or try again later.",
                    severity=SeverityLevel.ERROR,
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
        async with get_db_context() as db:
            res = await db.scalar(
                select(ScheduleSubscriber).where(
                    ScheduleSubscriber.guild_id == ctx.guild.id
                )
            )
            channel = self.client.get_channel(channel.id)

            if res.message_id is not None:
                msg = channel.get_partial_message(res.message_id)

            try:
                await db.execute(
                    delete(ScheduleSubscriber).where(
                        ScheduleSubscriber.id == str(res.id)
                    )
                )
                await db.commit()
            except Exception as e:
                logger.error(e)
                return

            if res.message_id is not None:
                await msg.delete()

            embed = generate_embed(
                title="Unsubscribing to comeback schedule success",
                content=f"The channel {channel.mention} has been unsubscribed from upcoming comebacks schedule.",
                severity=SeverityLevel.SUCCESS,
            )
            await ctx.send(embed=embed)

    @schedule.command(
        aliases=["list"], help="List all schedule subscribers", hidden=True
    )
    async def list_subscribers(self, ctx: Context):
        if ctx.author.id != settings.DISCORD_ADMIN_ID:
            return

        async with get_db_context() as db:
            res = (await db.scalars(select(ScheduleSubscriber))).all()
            subscribers = [ScheduleSubscriberSchema.model_validate(r) for r in res]
            return await ctx.send(
                "## Schedule subscribers\n\n"
                + f"**Count**: {len(subscribers)}\n"
                + "```json\n"
                + json.dumps([s.model_dump(mode="json") for s in subscribers], indent=2)
                + "\n```"
            )

    @schedule.command(help="Manually invoke schedule update", hidden=True)
    async def update(self, ctx: Context):
        logger.info("Manual schedule update invoked.")
        msg = await ctx.send("Updating schedule...")
        await self.update_schedule()
        await msg.delete()

    @staticmethod
    async def get_schedule() -> list[ComebackSchema]:
        logger.info("Fetching comeback schedule...")

        async with get_db_context() as db:
            res = await db.scalars(
                select(Comeback)
                .where(
                    cast(Comeback.date, DATE)
                    <= (func.now() + cast(timedelta(days=30), Interval))
                )
                .order_by(Comeback.date)
            )
            return [ComebackSchema.model_validate(r) for r in res.all()]

    @tasks.loop(
        time=[time(h, 0, 0, tzinfo=settings.DEFAULT_TZ) for h in [0, 6, 12, 18]]
    )
    async def update_schedule(self):
        schedule = await self.get_schedule()
        schedule_fields = generate_schedule_fields(schedule)
        logger.info("Updating comeback schedule...")

        async with get_db_context() as db:
            subscribers = (await db.scalars(select(ScheduleSubscriber))).all()

            for sub in subscribers:
                guild = self.client.get_guild(sub.guild_id)
                channel = guild.get_channel(sub.channel_id)
                msg = channel.get_partial_message(sub.message_id)
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
