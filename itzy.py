import os
import random
import twitter
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

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


HELP_MESSAGE = """
Hi! I am ITZYbot!

List of commands:
`!ping` : Check bot responsiveness.
`!help` : Show this help message.
`!ryujin`, `!yeji`, `!yuna`, `!lia`, `!chaeryeong` : Get a random pic of the member.
`!all`: Get a random pic from accounts that post all members.
`!random` : Get a random member.
"""


TARGET_CHANNEL = 726831180565184603


api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_SECRET'],
)


client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(name='ITZY fancams'))
    print(f'Logged in as {client.user}')
    hourly_itzy.start()

@client.command()
async def ping(ctx):
    await ctx.send(f'I am awake! ({round(client.latency*1000)}ms)')

@client.command()
async def itz(ctx, member):
    if member is None or member.upper() not in ITZY_ACCOUNTS:
        await ctx.send("That's not a member of ITZY :cry:")
        return
    account_cat = ITZY_ACCOUNTS[member.upper()]
    tl = api.GetUserTimeline(screen_name=random.choice(account_cat))
    media_post = (random.choice(tl)).media
    while media_post == None or len(media_post) == 0:
        media_post = random.choice(tl).media
    links = [media.media_url_https for media in media_post]
    for link in links:
        await ctx.send(link)

@client.command()
async def clear(ctx, amount):
    if amount == None or amount < 1:
        await ctx.send('Please specify a positive number.')
        return
    await ctx.channel.purge(limit=amount)

@tasks.loop(seconds=60*60)
async def hourly_itzy():
    channel = client.get_channel(TARGET_CHANNEL)
    print(f'Connected to channel {channel}')

    account_cat = random.choice(list(ITZY_ACCOUNTS.values()))
    tl = api.GetUserTimeline(screen_name=random.choice(account_cat))
    media_post = (random.choice(tl)).media
    while media_post == None or len(media_post) == 0:
        media_post = random.choice(tl).media
    links = [media.media_url_https for media in media_post]
    for link in links:
        await channel.send(link)

client.run(os.environ['DISCORD_TOKEN'])
