import re

from discord import Member, Message, User
from discord.ext import commands
from discord.ext.commands import Bot

from bot.api.internal import Api

EMOJI_PATTERN = re.compile(r"<a?:\w+:\d+>", re.I)
EMOJI_ID_PATTERN = re.compile(r"\d+")


class Stats(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client

    @staticmethod
    async def get_or_create_emote(body: dict):
        res = await Api.emote_cache(body["id"])
        if res.ok:
            emote = await res.json()
        else:
            res = await Api.emote_cache(None, "post", body)
            emote = await res.json()
        return emote

    @staticmethod
    async def get_or_create_sticker(body: dict):
        res = await Api.sticker_cache(body["id"])
        if res.ok:
            sticker = await res.json()
        else:
            res = await Api.sticker_cache(None, "post", body)
            sticker = await res.json()
        return sticker

    @staticmethod
    async def get_or_create_user(author: User | Member):
        res = await Api.user_cache(author.id)
        if res.ok:
            user = await res.json()
        else:
            res = await Api.user_cache(
                None,
                "post",
                {
                    "id": author.id,
                    "name": author.name,
                    "discriminator": author.discriminator,
                    "avatar": author.display_avatar.url,
                },
            )
            user = await res.json()
        return user

    @staticmethod
    async def send_emote_usage_stat(emote_id: int, user_id: int):
        await Api.emote_usage(None, "post", {"emote": emote_id, "user": user_id})

    @staticmethod
    async def send_sticker_usage_stat(sticker_id: int, user_id: int):
        await Api.sticker_usage(None, "post", {"sticker": sticker_id, "user": user_id})

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        emoji_matches = re.findall(EMOJI_PATTERN, message.content)

        if len(emoji_matches) > 0:
            for match in emoji_matches:
                id_match = re.search(EMOJI_ID_PATTERN, match)
                if id_match.group():
                    e_match = self.client.get_emoji(int(id_match.group()))
                    e_body = {
                        "id": e_match.id,
                        "guild_id": message.guild.id,
                        "channel_id": message.channel.id,
                        "name": e_match.name,
                        "url": e_match.url,
                    }

                    user = await self.get_or_create_user(message.author)
                    emote = await self.get_or_create_emote(e_body)
                    await self.send_emote_usage_stat(emote["id"], user["id"])

        if len(message.stickers) > 0:
            for sticker in message.stickers:
                s_body = {
                    "id": sticker.id,
                    "guild_id": message.guild.id,
                    "channel_id": message.channel.id,
                    "name": sticker.name,
                    "url": sticker.url,
                }
                user = await self.get_or_create_user(message.author)
                sticker = await self.get_or_create_sticker(s_body)
                await self.send_sticker_usage_stat(sticker["id"], user["id"])


async def setup(client: Bot):
    await client.add_cog(Stats(client))
