import os
import asyncio
from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks
from tqdm import tqdm

from .crud import *
from .utils import escape_quote, media_handler, bombard_hearts

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
        await ctx.channel.purge(limit=int(amount) + 1)


# Administrative functions

@client.command(help='Subscribe the channel to hourly updates of the selected group')
async def subscribe(ctx, group):
    api = ChannelApi()
    response = api.create(int(ctx.channel.id), group)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@client.command(help='Unsubscribe the channel to any hourly update')
async def unsubscribe(ctx):
    api = ChannelApi()
    response = api.delete(int(ctx.channel.id))
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@client.group(hidden=True)
async def admin(ctx):
    if str(ctx.message.author) != os.environ['DISCORD_ADMIN']:
        ctx.send('Sorry, you are not authorized to access that command.')
        return
    else:
        pass


@admin.command(help='Get technical bot status', hidden=True)
async def status(ctx):
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


@admin.group(hidden=True)
async def group(ctx):
    pass


@group.command(aliases=['get', 'read'], hidden=True)
async def group_get(ctx, name):
    api = GroupApi()
    response = api.get(name)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@group.command(aliases=['add', 'create'], hidden=True)
async def group_add(ctx, name):
    api = GroupApi()
    response = api.create(name)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@group.command(aliases=['edit', 'update'], hidden=True)
async def group_edit(ctx, old_name, new_name):
    api = GroupApi()
    response = api.update(old_name, new_name)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@admin.group(hidden=True)
async def member(ctx):
    pass


@member.command(aliases=['get', 'read'], hidden=True)
async def member_get(ctx, group, name):
    api = MemberApi()
    response = api.get(group, name)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@member.command(aliases=['add', 'create'], hidden=True)
async def member_add(ctx, *args):
    api = MemberApi()
    response = api.create(*args)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@admin.group(hidden=True)
async def account(ctx):
    pass


@account.command(aliases=['get'], hidden=True)
async def account_get(ctx, group, member):
    api = AccountApi()
    response = api.get(group, member)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@account.command(aliases=['create', 'add'], hidden=True)
async def account_add(ctx, *args):
    api = AccountApi()
    response = api.create(*args)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@account.command(aliases=['update', 'edit'], hidden=True)
async def account_edit(ctx, *args):
    api = AccountApi()
    response = api.update(*args)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@admin.group(hidden=True)
async def alias(ctx):
    pass


@alias.command(aliases=['get'], hidden=True)
async def alias_get(ctx, group, member):
    api = AliasApi()
    response = api.get(group, member)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@alias.command(aliases=['add', 'create'], hidden=True)
async def alias_add(ctx, *args):
    api = AliasApi()
    response = api.create(*args)
    message = f"```json\n{response}\n```"
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
                    await attachment.save(os.path.join(fp, f"{m_id}.{ext}"))
    print('Download complete.')


# Query functions

@client.command(aliases=['itzy'], help='Get a random pic of the specified ITZY member')
async def itz(ctx, *person):
    person = escape_quote(person)
    group = 'itzy'
    media = await media_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(aliases=['blackpink', 'mink', 'bp'], help='Get a random pic of the specified BLACKPINK member')
async def pink(ctx, *person):
    person = escape_quote(person)
    group = 'blackpink'
    media = await media_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(aliases=['twice'], help='Get a random pic of the specified TWICE member')
async def more(ctx, *person):
    person = escape_quote(person)
    group = 'twice'
    media = await media_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(aliases=['red-velvet', 'velvet', 'rv'], help='Get a random pic of the specified RED VELVET member')
async def red(ctx, *person):
    person = escape_quote(person)
    group = 'redvelvet'
    media = await media_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(help='Get a random pic of IU')
async def iu(ctx, *person):
    person = escape_quote(person)
    group = 'iu'
    media = await media_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(help='Get a random pic of the specified BTS member')
async def bts(ctx, *person):
    person = escape_quote(person)
    group = 'bts'
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


# Scheduled task deferrers

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


def run():
    client.run(os.environ['DISCORD_TOKEN'])


if __name__ == '__main__':
    run()
