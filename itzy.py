import os
import discord
import twitter
import random
from dotenv import load_dotenv

load_dotenv()

api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_SECRET'],
)

ACCOUNTS = {
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
`!wake` : Check if the bot is online.
`!help` : Show this help message.
`!ryujin`, `!yeji`, `!yuna`, `!lia`, `!chaeryeong` : Get a random pic of the member.
`!random` : Get a random member.
"""


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith('!'):
            query = message.content[1:]

            if query == 'wake':
                await message.channel.send('I am awake!')

            if query == 'help':
                await message.channel.send(HELP_MESSAGE)

            if query.upper() in ACCOUNTS.keys() or query.upper() == 'RANDOM':
                if query.upper() == 'RANDOM':
                    account_keys = list(ACCOUNTS.keys())
                    account_cat = ACCOUNTS[account_keys[random.randint(0, len(account_keys))]]
                else:
                    account_cat = ACCOUNTS[query.upper()]
                tl = api.GetUserTimeline(screen_name=account_cat[random.randint(0, len(account_cat))])
                media_post = tl[random.randint(0, len(tl))].media
                while media_post == None or len(media_post) == 0:
                    media_post = tl[random.randint(0, len(tl))].media
                links = [media.media_url_https for media in media_post]
                for link in links:
                    await message.channel.send(link)


client = MyClient()
client.run(os.environ['DISCORD_TOKEN'])
