import asyncio
import discord
from datetime import datetime
from discord.ext import commands, tasks
from django.conf import settings
from ..utils.endpoints import Api
from ..handlers.twitter import twitter_handler
from ..handlers.vlive import vlive_handler


class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client

    def cog_unload(self):
        self.hourly_itzy.cancel()
        self.hourly_twice.cancel()
        self.hourly_blackpink.cancel()
        self.vlive_listener.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.client.user}')
        activity_name = 'under development' if settings.DEBUG else f'in {len(self.client.guilds)} servers!'
        await self.client.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name=activity_name),
        )
        self.hourly_itzy.start()
        self.hourly_twice.start()
        self.hourly_blackpink.start()
        self.vlive_listener.start()

    async def send_hourly_to_channels(self, group: str):
        media, _group = await twitter_handler(group, [], True)
        while not media:
            media, _group = await twitter_handler(group, [], True)
        channels = _group['twitterMediaSubscribedChannels']
        for channel in channels:
            ch = self.client.get_channel(channel['channel_id'])
            print(f'Connected to {_group["name"]} channel {ch}')
            await ch.send(files=media)

    @tasks.loop(hours=1)
    async def hourly_itzy(self):
        group = 'itzy'
        await self.send_hourly_to_channels(group)

    @tasks.loop(hours=1)
    async def hourly_blackpink(self):
        group = 'blackpink'
        await self.send_hourly_to_channels(group)

    @tasks.loop(hours=1)
    async def hourly_twice(self):
        group = 'twice'
        await self.send_hourly_to_channels(group)

    @tasks.loop(seconds=30)
    async def vlive_listener(self):
        groups = await Api.groups()
        for group in groups:
            embed = await vlive_handler(group)
            if embed:
                channels = group['vliveSubscribedChannels']
                for channel in channels:
                    if settings.DEBUG and not channel['dev_channel']:
                        return
                    ch = self.client.get_channel(channel['channel_id'])
                    if ch:
                        await ch.send(embed=embed)

    @hourly_itzy.before_loop
    async def itzy_hour(self):
        now = datetime.now()
        if now.minute != 0:
            delta_min = 60 - now.minute
            print(f'Waiting for {delta_min} minutes to start hourly ITZY update...')
            await asyncio.sleep(delta_min * 60)
            print('Starting hourly ITZY update...')

    @hourly_blackpink.before_loop
    async def blackpink_hour(self):
        now = datetime.now()
        if now.minute != 30:
            if now.minute < 30:
                delta_min = 30 - now.minute
            else:
                delta_min = 90 - now.minute
            print(f'Waiting for {delta_min} minutes to start hourly BLACKPINK update...')
            await asyncio.sleep(delta_min * 60)
            print('Starting hourly BLACKPINK update...')

    @hourly_twice.before_loop
    async def twice_hour(self):
        now = datetime.now()
        if now.minute != 29:
            if now.minute < 29:
                delta_min = 29 - now.minute
            else:
                delta_min = (60 + 29) - now.minute
            print(f'Waiting for {delta_min} minutes to start hourly TWICE update...')
            await asyncio.sleep(delta_min * 60)
            print('Starting hourly TWICE update...')


def setup(client):
    client.add_cog(Tasks(client))
