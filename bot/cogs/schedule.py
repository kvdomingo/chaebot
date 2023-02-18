from datetime import datetime, time, timedelta
from http import HTTPStatus

from discord import Client, Color, Embed, TextChannel
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context
from django.conf import settings
from loguru import logger
from pytz import timezone

from bot.api.internal import Api

from ..firestore import get_firestore_client


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
            embed = Embed(
                title="Adding schedule subscription failed",
                description="due to the following error(s):",
                color=Color.red(),
            )
            for key, val in subscriber.items():
                embed.add_field(name=key, value=str(val), inline=False)
            embed.set_footer(text="Please check the errors above or try again later.")
            await ctx.send(embed=embed)
            return

        schedule = await self.get_schedule()
        schedule_strings = self.to_schedule_strings(schedule)
        embed = Embed(
            title="Upcoming comebacks",
            color=Color.blurple(),
            description="\n".join(schedule_strings),
        )
        embed.set_footer(text="KST | Shows the next 30 days of events")

        channel = ctx.guild.get_channel(channel.id)
        msg = await channel.send(embed=embed)
        res, status = await Api.schedule_subscribers(subscriber["id"], "patch", {"message_id": msg.id})
        if status != 200:
            embed = Embed(
                title="Adding schedule subscription failed",
                description="due to the following error(s):",
                color=Color.red(),
            )
            embed.set_footer(text="Please check the errors above or try again later.")
            for key, val in res.items():
                embed.add_field(name=key, value=str(val), inline=False)
            await msg.delete()
            await ctx.send(embed=embed)
            return

        embed = Embed(
            title="Adding schedule subscription success",
            description=f"The channel <#{channel}> has been subscribed to upcoming comebacks schedule.",
            color=Color.green(),
        )
        return await ctx.send(embed=embed)

    @schedule.command(aliases=["unsub"], help="Unsubscribe to upcoming comebacks calendar")
    async def unsubscribe(self, ctx: Context, channel: TextChannel):
        res = await Api.schedule_subscriber_from_guild(ctx.guild.id)
        channel = self.client.get_channel(channel.id)
        msg = channel.get_partial_message(res["message_id"])
        await msg.delete()
        await Api.schedule_subscribers(res["id"], "delete")
        embed = Embed(
            title="Unsubscribing to comeback schedule success",
            description=f"The channel <#{channel}> has been unsubscribed from upcoming comebacks schedule.",
            color=Color.green(),
        )
        await ctx.send(embed=embed)

    @staticmethod
    async def get_schedule():
        logger.info("Fetching comeback schedule...")
        db = get_firestore_client()
        coll_ref = (
            db.collection("comebacks")
            .order_by("date")
            .where("date", "<", datetime.now(timezone(settings.TIME_ZONE)) + timedelta(days=30))
        )
        return [doc.to_dict() async for doc in coll_ref.stream()]

    @staticmethod
    def to_schedule_strings(schedule: list[dict]) -> list[str]:
        logger.info("Formatting schedule strings...")
        if len(schedule) == 0:
            return ["None"]
        cb_strings = []
        for doc in schedule:
            dt: datetime = doc["date"].astimezone(timezone(settings.TIME_ZONE))
            dt_date = dt.strftime("%b %d")
            dt_time = dt.strftime("%H:%M")
            if dt.date() == datetime.now(timezone(settings.TIME_ZONE)).date():
                is_today = "`<today>`"
            else:
                is_today = ""
            descriptor = doc["album_type"]
            if not descriptor:
                if "japan" in doc["release"].lower():
                    descriptor = "Japan"
                elif doc["release"]:
                    descriptor = doc["release"]
                else:
                    descriptor = ""
            cb_strings.append(
                f"`[{dt_date} | {dt_time}]` **{doc['artist']}** {descriptor} 『{doc['album_title']}』 {is_today}"
            )
        return cb_strings

    @tasks.loop(time=[time(h, tzinfo=timezone(settings.TIME_ZONE)) for h in [0, 6, 12, 18]])
    async def update_schedule(self):
        schedule = await self.get_schedule()
        schedule_strings = self.to_schedule_strings(schedule)
        logger.info("Updating comeback schedule...")
        subscribers = await Api.schedule_subscribers()
        for sub in subscribers:
            guild = self.client.get_guild(sub["guild_id"])
            channel = guild.get_channel(sub["channel_id"])
            msg = channel.get_partial_message(sub["message_id"])
            embed = Embed(title="Upcoming comebacks", color=Color.blurple(), description="\n".join(schedule_strings))
            embed.set_footer(text="KST | Shows the next 30 days of events")
            await msg.edit(embed=embed)


async def setup(client: Bot):
    await client.add_cog(Schedule(client))
