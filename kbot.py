import os
import re
import io
import json
import random
import twitter
import discord
import asyncio
import aiohttp
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()

api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_SECRET'],
)


def alias_matcher(member, group, hourly):
    with open(f'{group}.json', 'r') as f:
        ACCOUNTS = json.load(f)

    if hourly:
        member = random.choice(list(ACCOUNTS.keys()))
        return ACCOUNTS[member]['accounts']

    member = ' '.join(member)

    if member is None or len(member) == 0:
        member = random.choice(list(ACCOUNTS.keys()))
        return ACCOUNTS[member]['accounts']

    for key in ACCOUNTS.keys():
        if re.search(member, key, re.I) or re.search(key, member, re.I):
            return ACCOUNTS[key]['accounts']

        for alias in ACCOUNTS[key]['aliases']:
            if re.search(alias, member, re.I) or re.search(member, alias, re.I):
                return ACCOUNTS[key]['accounts']

    member = random.choice(list(ACCOUNTS.keys()))
    return ACCOUNTS[member]['accounts']


async def media_handler(ctx, group, member=None, hourly=False):
    account_cat = alias_matcher(member, group, hourly)
    tl = api.GetUserTimeline(screen_name=random.choice(account_cat))

    media_post = (random.choice(tl)).media
    while media_post == None or len(media_post) == 0:
        media_post = random.choice(tl).media

    video_info = media_post[0].video_info
    if video_info is not None:
        if len(video_info['variants']) == 1:
            link = video_info['variants'][0]['url']
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as res:
                    if res.status != 200:
                        return
                    data = io.BytesIO(await res.read())
                    file = discord.File(data, 'image_0.mp4')
                    message = await ctx.send(file=file)
        else:
            for i, vid in enumerate(video_info['variants']):
                if '.m3u8' not in vid['url']:
                    link = vid['url']
                    async with aiohttp.ClientSession() as session:
                        async with session.get(link) as res:
                            if res.status != 200:
                                return
                            data = io.BytesIO(await res.read())
                            file = discord.File(data, 'video_0.mp4')
                            message = await ctx.send(file=file)
                    break
    else:
        links = [media.media_url_https for media in media_post]
        files = []
        async with aiohttp.ClientSession() as session:
            for i, link in enumerate(links):
                async with session.get(link) as res:
                    if res.status != 200:
                        return
                    data = io.BytesIO(await res.read())
                    files.append(discord.File(data, f'image_{i}.jpg'))
            message = await ctx.send(files=files)

    reactions = [
        '♥', '💘', '💖', '💗', '💓',
        '💙', '💚', '💛', '💜', '🧡',
        '💝', '💞', '💟', '🖤', '❤',
        '❣', '🤎', '🤍', '😍', '🥰',
    ]
    for react in reactions:
        await message.add_reaction(react)
        asyncio.sleep(1)


client = commands.Bot(command_prefix='!', description="Hi, I'm Botbot de Leon!")


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    hourly_itzy.start()
    hourly_blackpink.start()
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name='ITZY fancams'))


@client.command(help='Check server response time')
async def ping(ctx):
    await ctx.send(f'Pong ({round(client.latency*1000)}ms)')


@client.command(help='Get dyno metadata')
async def meta(ctx):
    created = os.environ['HEROKU_RELEASE_CREATED_AT']
    created = datetime.strptime(created, '%Y-%m-%dT%H:%M:%SZ')
    created += timedelta(hours=8)
    message = f"""
```
Latest release:
    {os.environ['HEROKU_RELEASE_VERSION']}
    {os.environ['HEROKU_SLUG_DESCRIPTION']}
    {created}
```
    """
    await ctx.send(message)


@client.command(help='(Re)start all hourly tasks')
async def wake(ctx):
    print('Starting all hourly tasks...')
    try:
        hourly_itzy.start()
        hourly_blackpink.start()
    except commands.errors.CommandInvokeError:
        await ctx.send('Already awake!')
    print('All scheduled tasks successfully started.')
    await ctx.send('I am awake! :sunrise:')
    await client.change_presence(status=discord.Status.online)


@client.command(help='Stop all hourly tasks')
async def sleep(ctx):
    if not (hourly_itzy.get_task() and hourly_blackpink.get_task()):
        await ctx.send('Already sleeping :sleeping:')
    else:
        print('Stopping all hourly tasks...')
        hourly_itzy.cancel()
        hourly_blackpink.cancel()
        print('All scheduled tasks successfully stopped.')
        await ctx.send('Going to sleep :sleeping:')
        await client.change_presence(status=discord.Status.idle)


@client.command(aliases=['itzy'], help='Get a random pic of the specified ITZY member')
async def itz(ctx, *person):
    group = 'itzy'
    await media_handler(ctx, group, person)


@client.command(aliases=['blackpink', 'mink', 'bp'], help='Get a random pic of the specified BLACKPINK member')
async def pink(ctx, *person):
    group = 'blackpink'
    await media_handler(ctx, group, person)


@client.command(aliases=['twice'], help='Get a random pic of the specified TWICE member')
async def more(ctx, *person):
    group = 'twice'
    await media_handler(ctx, group, person)


@client.command(aliases=['red-velvet', 'velvet', 'rv'], help='Get a random pic of the specified RED VELVET member')
async def red(ctx, *person):
    group = 'redvelvet'
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


@tasks.loop(hours=1)
async def hourly_blackpink():
    group = 'blackpink'
    channel = client.get_channel(int(os.environ['BLACKPINK_CHANNEL']))
    print(f'Connected to BLACKPINK channel {channel}')
    await media_handler(channel, group, member=None, hourly=True)


@hourly_itzy.before_loop
async def itzy_hour():
    now = datetime.now()
    if now.minute != 0:
        delta_min = 60 - now.minute
        print(f'Waiting for {delta_min} minutes to start hourly ITZY update...')
        await asyncio.sleep(delta_min * 60)
        print('Starting hourly ITZY update...')


@hourly_blackpink.before_loop
async def blackpink_hour():
    now = datetime.now()
    if now.minute != 0:
        delta_min = 60 - now.minute
        print(f'Waiting for {delta_min} minutes to start hourly BLACKPINK update...')
        await asyncio.sleep(delta_min * 60)
        print('Starting hourly BLACKPINK update...')


client.run(os.environ['DISCORD_TOKEN'])
