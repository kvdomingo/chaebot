import asyncio
import discord
from datetime import datetime
from discord.ext import commands, tasks
from src import DEBUG
from src.crud import *
from src.handlers.twitter import twitter_handler
from src.handlers.vlive import vlive_handler
from src.utils import bombard_hearts


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

        activity_name = 'under development' if DEBUG else f'in {len(self.client.guilds)} servers!'
        await self.client.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name=activity_name),
        )

        self.hourly_itzy.start()
        self.hourly_twice.start()
        self.hourly_blackpink.start()
        self.vlive_listener.start()

    async def send_hourly_to_channels(self, group: str):
        sess = Session()
        channels = sess.query(TwitterChannel).filter(TwitterChannel.group.has(name=group)).all()
        media = await twitter_handler(group, [], True)
        while not media:
            media = await twitter_handler(group, [], True)
        for channel in channels:
            ch = self.client.get_channel(channel.channel_id)
            print(group, ch)
            print(f'Connected to {group.upper()} channel {ch}')
            message = await ch.send(files=media)
            await bombard_hearts(message)
        sess.close_all()

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
        sess = Session()
        groups = sess.query(Group).all()
        for group in groups:
            embed = await vlive_handler(sess, group.name)
            if embed:
                channels = sess.query(VliveChannel).filter(VliveChannel.group.has(name=group.name)).all()
                for channel in channels:
                    ch = self.client.get_channel(channel.channel_id)
                    if ch:
                        await ch.send(embed=embed)
        sess.close_all()

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
