import os
import sys
from src import BASE_DIR
from discord.ext import commands, tasks
from tqdm import tqdm

MEDIA_DIR = BASE_DIR / 'src' / '_media'


class DownloaderBot(commands.Cog):
    def __init__(self, bot, limit):
        self.bot = bot
        self.limit = limit
        self.download.start()

    def cog_unload(self):
        self.download.cancel()

    async def general_downloader(self, group, channel, folders):
        limit = self.limit
        channel = self.bot.get_channel(channel)
        messages = await channel.history(limit=limit).flatten()
        for message in tqdm(messages):
            for attachment in message.attachments:
                m_id = str(attachment.id)
                ext = attachment.url.split('.')[-1]
                if ext != 'mp4':
                    existing_files = os.listdir(MEDIA_DIR)
                    for folder in folders:
                        existing_files.extend(os.listdir(MEDIA_DIR / group.lower() / folder))
                    if len(existing_files) > 0:
                        existing_files = [f.split('.')[0] for f in existing_files]
                    if m_id not in existing_files:
                        await attachment.save(MEDIA_DIR / group.lower() / f"{m_id}.{ext}")
        print(f'Download for {group.upper()} complete.')

    @tasks.loop(count=1)
    async def download(self):
        group = 'itzy'
        channel = 726831180565184603
        folders = ['yeji', 'lia', 'ryujin', 'chaeryeong', 'yuna', 'mixed']
        await self.general_downloader(group, channel, folders)

        group = 'twice'
        channel = 789385817884721164
        folders = [
            'nayeon', 'jeongyeon', 'momo', 'sana',
            'jihyo', 'mina', 'dahyun', 'chaeyoung',
            'tzuyu', 'mixed',
        ]
        await self.general_downloader(group, channel, folders)

    @download.before_loop
    async def before_download(self):
        await self.bot.wait_until_ready()

    @download.after_loop
    async def after_download(self):
        sys.exit()


def main(*args):
    limit, = args
    client = commands.Bot(command_prefix='!')
    client.add_cog(DownloaderBot(client, limit))
    client.run(os.environ.get('DISCORD_TOKEN'))


if __name__ == '__main__':
    main()
