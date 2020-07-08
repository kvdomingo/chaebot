import os, sys
sys.path.append('.')

from dotenv import load_dotenv
load_dotenv()

import django
django.setup()

import random
import discord
import asyncio
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from backend.utils import alias_matcher, media_handler


client = commands.Bot(command_prefix='!', description="Hi, I'm Botbot de Leon!")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    hourly_itzy.start()
    hourly_blackpink.start()


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
    else:
        await ctx.channel.purge(limit=int(amount + 1))


@tasks.loop(hours=1)
async def hourly_itzy():
    group = 'itzy'
    channel = client.get_channel(int(os.environ['ITZY_CHANNEL']))
    print(f'Connected to ITZY channel {channel}')
    await media_handler(channel, group, member=None, hourly=True)
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name='ITZY fancams'))


@tasks.loop(hours=1)
async def hourly_blackpink():
    group = 'blackpink'
    channel = client.get_channel(int(os.environ['BLACKPINK_CHANNEL']))
    print(f'Connected to BLACKPINK channel {channel}')
    await media_handler(channel, group, member=None, hourly=True)
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name='BLACKPINK fancams'))


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
    if now.minute != 30:
        if now.minute < 30:
            delta_min = 30 - now.minute
        else:
            delta_min = 90 - now.minute
        print(f'Waiting for {delta_min} minutes to start hourly BLACKPINK update...')
        await asyncio.sleep(delta_min * 60)
        print('Starting hourly BLACKPINK update...')


client.run(os.environ['DISCORD_TOKEN'])
