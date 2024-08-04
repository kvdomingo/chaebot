import asyncio
from datetime import datetime

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

from bot.api.internal import Api
from bot.handlers.hourly import hourly_handler
from kvisualbot.logging import logger


class Tasks(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client
        self.groups = Api.sync_groups()

    def cog_unload(self):
        self.hourly_itzy.cancel()
        self.hourly_twice.cancel()
        self.hourly_blackpink.cancel()
        self.hourly_red_velvet.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        self.hourly_itzy.start()
        self.hourly_twice.start()
        self.hourly_blackpink.start()
        self.hourly_red_velvet.start()

    async def send_hourly_to_channels(self, group: str, max_retries=10):
        media, _group = [], []
        for _ in range(max_retries):
            media, _group = await hourly_handler(group, [], True)
            if media:
                break
        if not media:
            return
        channels = _group["twitterMediaSubscribedChannels"]
        for channel in channels:
            ch = self.client.get_channel(channel["channel_id"])
            if not ch:
                return
            logger.info(f'Connected to {_group["name"]} channel {ch}')
            await ch.send(files=media)

    @tasks.loop(hours=1)
    async def hourly_itzy(self):
        group = "itzy"
        try:
            await self.send_hourly_to_channels(group)
        except discord.errors.HTTPException:
            await self.send_hourly_to_channels(group)

    @tasks.loop(hours=1)
    async def hourly_blackpink(self):
        group = "blackpink"
        await self.send_hourly_to_channels(group)

    @tasks.loop(hours=1)
    async def hourly_twice(self):
        group = "twice"
        await self.send_hourly_to_channels(group)

    @tasks.loop(hours=1)
    async def hourly_red_velvet(self):
        group = "red-velvet"
        await self.send_hourly_to_channels(group)

    @hourly_itzy.before_loop
    async def itzy_hour(self):
        now = datetime.now()
        if now.minute != 0:
            delta_min = 60 - now.minute
            logger.info(
                f"Waiting for {delta_min} minutes to start hourly ITZY update..."
            )
            await asyncio.sleep(delta_min * 60)
            logger.info("Starting hourly ITZY update...")

    @hourly_blackpink.before_loop
    async def blackpink_hour(self):
        now = datetime.now()
        if now.minute != 30:
            if now.minute < 30:
                delta_min = 30 - now.minute
            else:
                delta_min = 90 - now.minute
            logger.info(
                f"Waiting for {delta_min} minutes to start hourly BLACKPINK update..."
            )
            await asyncio.sleep(delta_min * 60)
            logger.info("Starting hourly BLACKPINK update...")

    @hourly_twice.before_loop
    async def twice_hour(self):
        now = datetime.now()
        if now.minute != 29:
            if now.minute < 29:
                delta_min = 29 - now.minute
            else:
                delta_min = (60 + 29) - now.minute
            logger.info(
                f"Waiting for {delta_min} minutes to start hourly TWICE update..."
            )
            await asyncio.sleep(delta_min * 60)
            logger.info("Starting hourly TWICE update...")

    @hourly_red_velvet.before_loop
    async def red_velvet_hour(self):
        now = datetime.now()
        if now.minute != 5:
            if now.minute < 5:
                delta_min = 5 - now.minute
            else:
                delta_min = (60 + 5) - now.minute
            logger.info(
                f"Waiting for {delta_min} minutes to start hourly Red Velvet update..."
            )
            await asyncio.sleep(delta_min * 60)
            logger.info("Starting hourly Red Velvet update...")


async def setup(_):
    pass
