import os
import json
import random
import twitter
import discord
import asyncio
from discord.ext import commands, tasks
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_SECRET'],
)


async def media_handler(ctx, group, member=None, hourly=False):
    with open(f'{group}.json', 'r') as f:
        ACCOUNTS = json.load(f)

    if hourly:
        member = random.choice(list(ACCOUNTS.keys()))
    else:
        member = (''.join(member)).lower()

        if member is None or len(member) == 0:
            member = random.choice(list(ACCOUNTS.keys()))

        if member.upper() in ACCOUNTS.keys():
            member = member.upper()
        else:
            person = None
            for key in ACCOUNTS.keys():
                if member in ACCOUNTS[key]['aliases']:
                    person, member = key, key
                    break
            if person is None:
                member = random.choice(list(ACCOUNTS.keys()))

    account_cat = ACCOUNTS[member.upper()]['accounts']
    tl = api.GetUserTimeline(screen_name=random.choice(account_cat))

    media_post = (random.choice(tl)).media
    while media_post == None or len(media_post) == 0:
        media_post = random.choice(tl).media

    video_info = media_post[0].video_info
    if video_info is not None:
        for i, vid in enumerate(video_info['variants']):
            if '.m3u8' not in vid['url']:
                link = vid['url']
                break
        await ctx.send(link)
    else:
        links = [media.media_url_https for media in media_post]
        for link in links:
            await ctx.send(link)


client = commands.Bot(command_prefix='!', description="Hi, I'm Botbot de Leon!")


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    hourly_itzy.start()
    hourly_blackpink.start()


@client.command(aliases=['wake'], help='Check server response time')
async def ping(ctx):
    await ctx.send(f'I am awake! ({round(client.latency*1000)} ms)')


@client.command(help='Get a random pic of the specified ITZY member')
async def itz(ctx, *person):
    group = 'itzy'
    await media_handler(ctx, group, person)


@client.command(help='Get a random pic of the specified BLACKPINK member')
async def pink(ctx, *person):
    group = 'blackpink'
    await media_handler(ctx, group, person)


@client.command(help='Clear the specified amount of latest messages')
async def clear(ctx, amount):
    if amount == None or int(amount) < 1:
        await ctx.send('Please specify a positive number.')
        return
    await ctx.channel.purge(limit=int(amount))


@tasks.loop(hours=1)
async def hourly_itzy():
    group = 'itzy'
    channel = client.get_channel(int(os.environ['ITZY_CHANNEL']))
    print(f'Connected to ITZY channel {channel}')
    await media_handler(channel, group, member=None, hourly=True)
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(name='ITZY fancams'))


@tasks.loop(hours=1)
async def hourly_blackpink():
    group = 'blackpink'
    channel = client.get_channel(int(os.environ['BLACKPINK_CHANNEL']))
    print(f'Connected to BLACKPINK channel {channel}')
    await media_handler(channel, group, member=None, hourly=True)
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(name='BLACKPINK fancams'))


@hourly_itzy.before_loop
async def itzy_hour00():
    now = datetime.now()
    if now.minute != 0:
        delta_min = 60 - now.minute
        print(f'Waiting for {delta_min} minutes to start hourly ITZY update...')
        await asyncio.sleep(delta_min * 60)
        print('Starting hourly ITZY update...')


@hourly_blackpink.before_loop
async def blackpink_hour30():
    now = datetime.now()
    if now.minute != 30:
        if now.minute < 30:
            delta_min = 30 - now.minute
        elif now.minute > 30:
            delta_min = 90 - now.minute
        print(f'Waiting for {delta_min} minutes to start hourly BLACKPINK update...')
        await asyncio.sleep(delta_min * 60)
        print('Starting hourly BLACKPINK update...')


client.run(os.environ['DISCORD_TOKEN'])
