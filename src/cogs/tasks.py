import io
import aiohttp
import asyncio
import discord
from datetime import datetime
from discord.ext import commands, tasks
from src.crud import *
from src.handlers.twitter import media_handler as twitter_handler
from src.handlers.vlive import loop_handler as vlive_handler
from src.utils import bombard_hearts


class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client

    def cog_unload(self):
        self.hourly_itzy.cancel()
        self.hourly_blackpink.cancel()
        self.vlive_listener.cancel()
        self.twohour_covid.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.client.user}')
        self.hourly_itzy.start()
        self.hourly_blackpink.start()
        self.vlive_listener.start()
        self.twohour_covid.start()

    async def send_hourly_to_channels(self, group: str):
        sess = Session()
        channels = sess.query(TwitterChannel).filter(TwitterChannel.group.has(name=group)).all()
        media = await twitter_handler(group, [], True)
        for channel in channels:
            ch = self.client.get_channel(channel.channel_id)
            print(f'Connected to {group.upper()} channel {ch}')
            message = await ch.send(files=media)
            await bombard_hearts(message)
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name=f'{group.upper()} fancams'))
        sess.close_all()

    @tasks.loop(hours=1)
    async def hourly_itzy(self):
        group = 'itzy'
        await self.send_hourly_to_channels(group)

    @tasks.loop(hours=1)
    async def hourly_blackpink(self):
        group = 'blackpink'
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
        if now.minute < 30:
            await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name='ITZY fancams'))

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
        if now.minute > 30:
            await self.client.change_presence(
                status=discord.Status.online,
                activity=discord.Game(name='BLACKPINK fancams')
            )

    @tasks.loop(hours=6)
    async def twohour_covid(self):
        img_url = 'https://res.cloudinary.com/kdphotography-assets/image/upload/v1/kvisualbot/covidph.jpg'
        ch = self.client.get_channel(695937463742496800)
        async with aiohttp.ClientSession() as session:
            async with session.get(img_url) as res:
                data = io.BytesIO(await res.read())
                file = discord.File(data, 'covidph.jpg')
        await ch.send('<@696695544826953769>')
        await ch.send(file=file)


def setup(client):
    client.add_cog(Tasks(client))
