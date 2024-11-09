import json
from datetime import datetime

import aiohttp
from discord import Color, Embed, Interaction
from discord.app_commands import Group, command
from loguru import logger


class Mama(Group):
    BASE_URL = "https://api.2022mama.com/api/mama2022/polls"

    @command(description="Worldwide Fans' Choice Category")
    async def worldwide(self, itx: Interaction):
        poll_id = "A7aLeR4or8"
        endpoint = f"{self.BASE_URL}/{poll_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as res:
                if not res.ok:
                    raise ConnectionError
                try:
                    top = await res.read()
                    top = top.decode("utf-8")
                    top = json.loads(top)["data"]
                except json.JSONDecodeError as e:
                    logger.error(f"{res.status} {e}:\n{top}")
                    return await itx.response.send_message("`MAMA API Error`")

        embed = Embed(
            title="MAMA 2022 Current Voting Results - Worldwide Fans' Choice Top 10",
            url="https://2022mama.com/vote",
            color=Color.gold(),
            description=f"Total number of votes: {top['voteCount']:,}",
        )
        last_updated = datetime.strptime(
            top["voteCountUpdatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        embed.set_footer(
            text=f"Last updated {last_updated.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        for i, artist in enumerate(top["pollOptions"]):
            embed.add_field(
                name=f"{i+1}. {artist['name_en']}",
                value=f"{artist['votePercentage']}%",
                inline=True,
            )

        embed.set_image(
            url=f"https://2022mama.com{top['pollOptions'][0]['featuredImage']}"
        )
        await itx.response.send_message(embed=embed)


# mama = Mama()


async def setup(_):
    pass
