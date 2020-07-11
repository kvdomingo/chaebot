import os
import discord
import asyncio
from tqdm import tqdm
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from .utils import alias_matcher, media_handler, bombard_hearts
from .models import *
from . import Session


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
client = commands.Bot(command_prefix='!', description="Hi, I'm Botbot de Leon!")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    hourly_itzy.start()
    hourly_blackpink.start()


# Convenience functions

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


@client.command(help='Clear the specified amount of latest messages')
async def clear(ctx, amount):
    if amount == None or int(amount) < 1:
        await ctx.send('Please specify a positive number.')
    else:
        await ctx.channel.purge(limit=int(amount + 1))


# Administrative functions

@client.command(aliases=['get-aliases'], hidden=True)
async def get_aliases(ctx, group, member):
    from .asyncers import sta_get_alias
    message = await sta_get_alias(group, member)
    await ctx.send(message)


@client.command(aliases=['add-alias'], hidden=True)
async def add_alias(ctx, group, member, *alias):
    from .asyncers import sta_add_alias
    message = await sta_add_alias(group, member, alias)
    await ctx.send(message)


@client.command(hidden=True)
async def download(ctx, limit):
    if limit.lower() == 'all':
        limit = None
    else:
        limit = int(limit)
    await ctx.channel.purge(limit=1)
    messages = await ctx.channel.history(limit=limit).flatten()
    for message in tqdm(messages):
        for attachment in message.attachments:
            m_id = attachment.id
            ext = attachment.url.split('.')[-1]
            if ext != 'mp4':
                fp = os.path.join(BASE_DIR, 'src/_media')
                existing_files = os.listdir(fp)
                if len(existing_files) > 0:
                    existing_files = [f.split('.')[0] for f in existing_files]
                if str(m_id) not in existing_files:
                    await attachment.save(os.path.join(fp, f'{m_id}.{ext}'))
    print('Download complete.')


# Query functions

@client.command(aliases=['itzy'], help='Get a random pic of the specified ITZY member')
async def itz(ctx, *person):
    group = 'itzy'
    media = await media_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(aliases=['blackpink', 'mink', 'bp'], help='Get a random pic of the specified BLACKPINK member')
async def pink(ctx, *person):
    group = 'blackpink'
    media = await media_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(aliases=['twice'], help='Get a random pic of the specified TWICE member')
async def more(ctx, *person):
    group = 'twice'
    media = await media_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(aliases=['red-velvet', 'velvet', 'rv'], help='Get a random pic of the specified RED VELVET member')
async def red(ctx, *person):
    group = 'redvelvet'
    media = await media_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


# Scheduled tasks

@tasks.loop(hours=1)
async def hourly_itzy():
    sess = Session()
    group = 'itzy'
    channels = sess.query(Channel).filter(Channel.group.has(name=group)).all()
    media = await media_handler(group, member=None, hourly=True)
    for channel in channels:
        ch = client.get_channel(channel.channel_id)
        print(f'Connected to ITZY channel {ch}')
        message = await ch.send(files=media)
        await bombard_hearts(message)
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name='ITZY fancams'))
    sess.close_all()


@tasks.loop(hours=1)
async def hourly_blackpink():
    sess = Session()
    group = 'blackpink'
    channels = sess.query(Channel).filter(Channel.group.has(name=group)).all()
    media = await media_handler(group, member=None, hourly=True)
    for channel in channels:
        ch = client.get_channel(channel.channel_id)
        print(f'Connected to BLACKPINK channel {ch}')
        message = await ch.send(files=media)
        await bombard_hearts(message)
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name='BLACKPINK fancams'))
    sess.close_all()


# Schedule deferrers

@hourly_itzy.before_loop
async def itzy_hour():
    now = datetime.now()
    if now.minute != 0:
        delta_min = 60 - now.minute
        print(f'Waiting for {delta_min} minutes to start hourly ITZY update...')
        await asyncio.sleep(delta_min * 60)
        print('Starting hourly ITZY update...')
    if now.minute < 30:
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name='ITZY fancams'))


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
    if now.minute > 30:
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name='BLACKPINK fancams'))


client.run(os.environ['DISCORD_TOKEN'])
