import os
import sys
from discord.ext import commands, tasks
from tqdm import tqdm

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(BASE_DIR, 'src/_media')


class DownloaderBot(commands.Cog):
    def __init__(self, bot, limit, channel):
        self.bot = bot
        self.limit = limit
        self.channel = channel
        self.downloader.start()

    def cog_unload(self):
        self.downloader.cancel()

    @tasks.loop(count=1)
    async def downloader(self):
        limit, channel = self.limit, self.channel
        channel = self.bot.get_channel(channel)
        messages = await channel.history(limit=limit).flatten()
        folders = ['yeji', 'lia', 'ryujin', 'chaeryeong', 'yuna', 'mixed']
        for message in tqdm(messages):
            for attachment in message.attachments:
                m_id = str(attachment.id)
                ext = attachment.url.split('.')[-1]
                if ext != 'mp4':
                    existing_files = os.listdir(MEDIA_DIR)
                    for folder in folders:
                        existing_files.extend(os.listdir(os.path.join(MEDIA_DIR, folder)))
                    if len(existing_files) > 0:
                        existing_files = [f.split('.')[0] for f in existing_files]
                    if m_id not in existing_files:
                        await attachment.save(os.path.join(MEDIA_DIR, f"{m_id}.{ext}"))
        print('Download complete.')

    @downloader.before_loop
    async def before_download(self):
        await self.bot.wait_until_ready()

    @downloader.after_loop
    async def after_download(self):
        sys.exit(0)


def main(*args):
    limit, channel = args
    client = commands.Bot(command_prefix='!')
    client.add_cog(DownloaderBot(client, limit, channel))
    client.run(os.environ['DISCORD_TOKEN'])


if __name__ == '__main__':
    main()
