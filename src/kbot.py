import os
import asyncio
from datetime import datetime, timedelta
from random import SystemRandom

import discord
from discord.ext import commands, tasks
from tqdm import tqdm

from .crud import *
from .utils import bombard_hearts, escape_quote
from src.handlers.twitter import twitter_handler
from src.handlers.vlive import vlive_handler


random = SystemRandom()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
client = commands.Bot(command_prefix='!', description="Hi, I'm Botbot de Leon!")


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    hourly_itzy.start()
    hourly_blackpink.start()
    itzy_vlive.start()


# Convenience functions

@client.command(help='Check server response time')
async def ping(ctx):
    await ctx.send(f'Pong ({round(client.latency*1000)}ms)')


@client.command(help='Clear the specified amount of latest messages')
async def clear(ctx, amount: int = 0):
    if amount < 1:
        await ctx.send('Please specify a positive number.')
    else:
        await ctx.channel.purge(limit=amount+1)


# Administrative functions

@client.group(hidden=True)
async def twitter():
    pass


@twitter.command(aliases=['subscribe'], help='Subscribe the channel to hourly updates of the selected group')
async def twitter_subscribe(ctx, group: str):
    response = TwitterChannelApi().create(ctx.channel.id, group)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@twitter.command(aliases=['unsubscribe'], help='Unsubscribe the channel to any hourly update')
async def twitter_unsubscribe(ctx):
    response = TwitterChannelApi().delete(ctx.channel.id)
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
    response = GroupApi().get(name)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@group.command(aliases=['add', 'create'], hidden=True)
async def group_add(ctx, name, vlive_channel_code=None, vlive_channel_seq=None, vlive_last_seq=None):
    kwargs = {k: v for k, v in list(locals().items())[1:]}
    response = GroupApi().create(**kwargs)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@group.command(aliases=['edit', 'update'], hidden=True)
async def group_edit(ctx, old_name, new_name):
    response = GroupApi().update(old_name, new_name)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@group.command(aliases=['subscribe'], help='Subscribe the channel to VLIVE notifications of the selected group')
async def group_subscribe(ctx, name: str):
    response = VliveChannelApi().create(ctx.channel.id, name)
    message = f"```\n{response}\n```"
    await ctx.send(message)


@group.command(aliases=['unsubscribe'], help='Unsubscribe the channel to all VLIVE notifications')
async def group_unsubscribe(ctx):
    response = VliveChannelApi().delete(ctx.channel.id)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@admin.group(hidden=True)
async def member(ctx):
    pass


@member.command(aliases=['get', 'read'], hidden=True)
async def member_get(ctx, group, name):
    response = MemberApi().get(group, name)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@member.command(aliases=['add', 'create'], hidden=True)
async def member_add(ctx, group, stage_name, family_name, given_name):
    kwargs = {k: v for k, v in list(locals().items())[1:]}
    response = MemberApi().create(**kwargs)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@admin.group(hidden=True)
async def account(ctx):
    pass


@account.command(aliases=['get'], hidden=True)
async def account_get(ctx, group, member):
    response = AccountApi().get(group, member)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@account.command(aliases=['create', 'add'], hidden=True)
async def account_add(ctx, group, member, account_name):
    kwargs = {k: v for k, v in list(locals().items())[1:]}
    response = AccountApi().create(**kwargs)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@account.command(aliases=['update', 'edit'], hidden=True)
async def account_edit(ctx, group, member, old_account, new_account):
    kwargs = {k: v for k, v in list(locals().items())[1:]}
    response = AccountApi().update(**kwargs)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@admin.group(hidden=True)
async def alias(ctx):
    pass


@alias.command(aliases=['get'], hidden=True)
async def alias_get(ctx, group, member):
    response = AliasApi().get(group, member)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@alias.command(aliases=['add', 'create'], hidden=True)
async def alias_add(ctx, group, member, alias):
    response = AliasApi().create(group, member, alias)
    message = f"```json\n{response}\n```"
    await ctx.send(message)


@client.command(hidden=True)
async def download(ctx, limit: str):
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

@client.command(help='Get a random pic from a random JYP group')
async def jyp(ctx):
    group = random.choice([itzy, twice])
    await group(ctx, [])


@client.command(aliases=['itz'], help='Get a random pic of the specified ITZY member')
async def itzy(ctx, *person):
    person = escape_quote(person)
    group = 'itzy'
    media = await twitter_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(aliases=['pink', 'mink', 'bp'], help='Get a random pic of the specified BLACKPINK member')
async def blackpink(ctx, *person):
    person = escape_quote(person)
    group = 'blackpink'
    media = await twitter_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(aliases=['more'], help='Get a random pic of the specified TWICE member')
async def twice(ctx, *person):
    person = escape_quote(person)
    group = 'twice'
    media = await twitter_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(
    aliases=['red-velvet', 'red', 'velvet', 'rv'],
    help='Get a random pic of the specified RED VELVET member'
)
async def red_velvet(ctx, *person):
    person = escape_quote(person)
    group = 'redvelvet'
    media = await twitter_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(help='Get a random pic of IU')
async def iu(ctx, *person):
    person = escape_quote(person)
    group = 'iu'
    media = await twitter_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(aliases=['bangtan'], help='Get a random pic of the specified BTS member')
async def bts(ctx, *person):
    person = escape_quote(person)
    group = 'bts'
    media = await twitter_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(aliases=['mama'], help='Get a random pic of the specified MAMAMOO member')
async def mamamoo(ctx, *person):
    person = escape_quote(person)
    group = 'mamamoo'
    media = await twitter_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


# Scheduled tasks

@tasks.loop(hours=1)
async def hourly_itzy():
    sess = Session()
    group = 'itzy'
    channels = sess.query(TwitterChannel).filter(TwitterChannel.group.has(name=group)).all()
    media = await twitter_handler(group, '', True)
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
    channels = sess.query(TwitterChannel).filter(TwitterChannel.group.has(name=group)).all()
    media = await twitter_handler(group, '', True)
    for channel in channels:
        ch = client.get_channel(channel.channel_id)
        print(f'Connected to BLACKPINK channel {ch}')
        message = await ch.send(files=media)
        await bombard_hearts(message)
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name='BLACKPINK fancams'))
    sess.close_all()


@tasks.loop(seconds=30)
async def itzy_vlive():
    print("Checking latest ITZY VLIVE...")
    sess = Session()
    group = 'itzy'
    embed = vlive_handler(sess, group)
    if embed:
        channels = sess.query(VliveChannel).filter(VliveChannel.group.has(name=group)).all()
        for channel in channels:
            ch = client.get_channel(channel.channel_id)
            await ch.send(f"@everyone ITZY is live!")
            await ch.send(embed=embed)
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
