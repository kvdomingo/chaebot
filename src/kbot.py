import os
import asyncio
import logging
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from random import SystemRandom
from .crud import *
from .utils import bombard_hearts, escape_quote
from src.handlers.twitter import media_handler as twitter_handler
from src.handlers.vlive import loop_handler as vlive_handler

logging.basicConfig(level=logging.INFO)
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
    await ctx.send(f'Pong ({round(client.latency * 1000)}ms)')


@client.command(help='Clear the specified amount of latest messages')
async def clear(ctx, amount: int = 0):
    if amount < 1:
        await ctx.send('Please specify a positive number.')
    else:
        await ctx.channel.purge(limit=amount + 1)


# (Un)Subscription functions

@client.group(hidden=True)
async def twitter(ctx):
    pass


@twitter.command(aliases=['subscribe'], help='Subscribe the channel to hourly updates of the selected group')
async def twitter_subscribe(ctx, group: str):
    message = TwitterChannelApi().create(ctx.channel.id, group)
    await ctx.send(message)


@twitter.command(aliases=['unsubscribe'], help='Unsubscribe the channel to any hourly update')
async def twitter_unsubscribe(ctx, group: str):
    message = TwitterChannelApi().delete(ctx.channel.id, group)
    await ctx.send(message)


@client.group(hidden=True)
async def vlive(ctx):
    pass


@vlive.command(aliases=['subscribe'], help='Subscribe the channel to VLIVE notifications of the selected group')
async def vlive_subscribe(ctx, name: str):
    message = VliveChannelApi().create(ctx.channel.id, name)
    await ctx.send(message)


@vlive.command(aliases=['unsubscribe'], help='Unsubscribe the channel to all VLIVE notifications')
async def vlive_unsubscribe(ctx):
    message = VliveChannelApi().delete(ctx.channel.id)
    await ctx.send(message)


# Administrative functions

@client.group(hidden=True)
async def admin(ctx):
    if str(ctx.message.author) != os.environ['DISCORD_ADMIN']:
        ctx.send('Sorry, you are not authorized to access that command.')
        return
    else:
        pass


@admin.command(aliases=['status'], help='Get technical bot status', hidden=True)
async def admin_status(ctx):
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


@admin.group(aliases=['group'], hidden=True)
async def admin_group(ctx):
    pass


@admin_group.command(aliases=['get', 'read'], hidden=True)
async def group_get(ctx, name=None):
    response = GroupApi().get(name)
    await ctx.send(response)


@admin_group.command(aliases=['add', 'create'], hidden=True)
async def group_add(ctx, name, vlive_channel_code=None, vlive_channel_seq=None, vlive_last_seq=None):
    kwargs = {k: v for k, v in list(locals().items())[1:]}
    message = GroupApi().create(**kwargs)
    await ctx.send(message)


@admin_group.command(aliases=['edit', 'update'], hidden=True)
async def group_edit(ctx, old_name, new_name):
    message = GroupApi().update(old_name, new_name)
    await ctx.send(message)


@admin.group(aliases=['member'], hidden=True)
async def admin_member(ctx):
    pass


@admin_member.command(aliases=['get', 'read'], hidden=True)
async def member_get(ctx, group, name):
    message = MemberApi().get(group, name)
    await ctx.send(message)


@admin_member.command(aliases=['add', 'create'], hidden=True)
async def member_add(ctx, group, stage_name, family_name, given_name):
    kwargs = {k: v for k, v in list(locals().items())[1:]}
    message = MemberApi().create(**kwargs)
    await ctx.send(message)


@admin.group(aliases=['account'], hidden=True)
async def admin_account(ctx):
    pass


@admin_account.command(aliases=['get'], hidden=True)
async def account_get(ctx, group, member):
    message = AccountApi().get(group, member)
    await ctx.send(message)


@admin_account.command(aliases=['create', 'add'], hidden=True)
async def account_add(ctx, group, member, account_name):
    kwargs = {k: v for k, v in list(locals().items())[1:]}
    message = AccountApi().create(**kwargs)
    await ctx.send(message)


@admin_account.command(aliases=['update', 'edit'], hidden=True)
async def account_edit(ctx, group, member, old_account, new_account):
    kwargs = {k: v for k, v in list(locals().items())[1:]}
    message = AccountApi().update(**kwargs)
    await ctx.send(message)


@admin.group(aliases=['alias'], hidden=True)
async def admin_alias(ctx):
    pass


@admin_alias.command(aliases=['get'], hidden=True)
async def alias_get(ctx, group, member):
    message = AliasApi().get(group, member)
    await ctx.send(message)


@admin_alias.command(aliases=['add', 'create'], hidden=True)
async def alias_add(ctx, group, member, alias):
    message = AliasApi().create(group, member, alias)
    await ctx.send(message)


# Query functions

@client.command(help='Get a random pic from a random JYP group')
async def jyp(ctx):
    group = random.choice([itzy, twice])
    await group(ctx, '')


@client.command(aliases=['itz'], help='Get a random pic of the specified ITZY member')
async def itzy(ctx, *person: str):
    person = escape_quote(person)
    group = 'itzy'
    media = await twitter_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(aliases=['pink', 'mink', 'bp'], help='Get a random pic of the specified BLACKPINK member')
async def blackpink(ctx, *person: str):
    person = escape_quote(person)
    group = 'blackpink'
    media = await twitter_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(aliases=['more'], help='Get a random pic of the specified TWICE member')
async def twice(ctx, *person: str):
    person = escape_quote(person)
    group = 'twice'
    media = await twitter_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(
    aliases=['red-velvet', 'red', 'velvet', 'rv'],
    help='Get a random pic of the specified RED VELVET member'
)
async def red_velvet(ctx, *person: str):
    person = escape_quote(person)
    group = 'redvelvet'
    media = await twitter_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(help='Get a random pic of IU')
async def iu(ctx, *person: str):
    person = escape_quote(person)
    group = 'iu'
    media = await twitter_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(aliases=['bangtan'], help='Get a random pic of the specified BTS member')
async def bts(ctx, *person: str):
    person = escape_quote(person)
    group = 'bts'
    media = await twitter_handler(group, person)
    message = await ctx.send(files=media)
    await bombard_hearts(message)


@client.command(aliases=['mama'], help='Get a random pic of the specified MAMAMOO member')
async def mamamoo(ctx, *person: str):
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
    media = await twitter_handler(group, [], True)
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
    media = await twitter_handler(group, [], True)
    for channel in channels:
        ch = client.get_channel(channel.channel_id)
        print(f'Connected to BLACKPINK channel {ch}')
        message = await ch.send(files=media)
        await bombard_hearts(message)
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name='BLACKPINK fancams'))
    sess.close_all()


@tasks.loop(seconds=30)
async def itzy_vlive():
    sess = Session()
    group = 'itzy'
    embed = vlive_handler(sess, group)
    if embed:
        channels = sess.query(VliveChannel).filter(VliveChannel.group.has(name=group)).all()
        for channel in channels:
            ch = client.get_channel(channel.channel_id)
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
