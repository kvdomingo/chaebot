import os
import random
import twitter
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

ALIASES = {
    'RANDOM': [
        'sisi',
        'bayan ko',
        'bayan',
        'mahusay',
        'bayan',
        'husay',
        'huhusay',
    ],
    'RYUJIN': [
        'ryujin',
        'joanne',
    ],
    'LIA': [
        'lia',
        'julia',
        'jisu',
        'jisoo',
        'choi',
    ],
    'YUNA': [
        'yuna',
        'hussey',
    ],
    'YEJI': [
        'yeji',
        'lucy',
    ],
    'CHAERYEONG': [
        'chaeryeong',
        'ryeong',
        'judy',
    ],
}


ITZY_ACCOUNTS = {
    'ALL': [
        'archiveitzy',
        'ITZYofficial',
    ],
    'RYUJIN': [
        'ryujinpics',
        'shinryujinpic',
        'hourlyryu',
    ],
    'LIA': [
        'hourlylia',
        'liarchive',
    ],
    'YUNA': [
        'yunaspics',
        'yunasarchive',
        'picyuna',
        'littIeyuna',
    ],
    'YEJI': [
        'hourlyyeji',
        'yejigallery',
        'yejiarchives',
    ],
    'CHAERYEONG': [
        'chaerpics',
    ],
}


api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_SECRET'],
)


async def media_handler(ctx, member, **kwargs):
    account_cat = ITZY_ACCOUNTS[member.upper()]
    tl = api.GetUserTimeline(screen_name=random.choice(account_cat))

    media_post = (random.choice(tl)).media
    while media_post == None or len(media_post) == 0:
        media_post = random.choice(tl).media

    video_info = media_post[0].video_info
    if video_info is not None:
        if len(video_info['variants']) > 1:
            link = video_info['variants'][1]['url']
        else:
            link = video_info['variants'][0]['url']
        await ctx.send(link)
    else:
        links = [media.media_url_https for media in media_post]
        for link in links:
            await ctx.send(link)


client = commands.Bot(command_prefix='!', description="Hi, I'm ITZYbot!")


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(name='ITZY fancams'))
    print(f'Logged in as {client.user}')
    hourly_itzy.start()


@client.command(aliases=['wake'], help='Check server response time')
async def ping(ctx):
    await ctx.send(f'I am awake! ({round(client.latency*1000)} ms)')


@client.command(help='Get a random pic of the specified member')
async def itz(ctx, person):
    if person is None:
        member = random.choice(ITZY_ACCOUNTS.keys())
        await media_handler(ctx, member)

    if person.upper() in ITZY_ACCOUNTS.keys():
        member = person.upper()
        await media_handler(ctx, member)
    else:
        member = None
        for key in ALIASES.keys():
            if person in ALIASES[key]:
                member = key
                break
        if member is None:
            ctx.send("Sorry, I don't recognize that member or alias :cry:")
            return
        await media_handler(ctx, member)

@client.command(aliases=['get-aliases'], help='Get a list of member aliases')
async def get_aliases(ctx, *args):
    if len(args) == 0:
        message = '```\n'
        for key, val in ALIASES.items():
            message += f'{key}: {", ".join(val)}\n'
        message += '\n```'
        await ctx.send(message)
    elif len(args) == 1:
        args[0] = args[0].upper()
        message = f'```\n{args[0]}: {ALIASES[args[0]]}\n```'
        await ctx.send(message)


@client.command(help='Clear the specified amount of latest messages')
async def clear(ctx, amount):
    if amount == None or int(amount) < 1:
        await ctx.send('Please specify a positive number.')
        return
    await ctx.channel.purge(limit=int(amount))


@tasks.loop(seconds=60*60)
async def hourly_itzy():
    channel = client.get_channel(int(os.environ['TARGET_CHANNEL']))
    print(f'Connected to channel {channel}')

    member = random.choice(list(ITZY_ACCOUNTS.keys()))
    media_handler(channel, member)


client.run(os.environ['DISCORD_TOKEN'])
