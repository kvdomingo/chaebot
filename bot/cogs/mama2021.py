import json
import aiohttp
import discord
from discord.ext import commands
from bot.utils.query import query_string_from_dict


class Mama2021(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.base_url = "https://mama.mwave.me/en/api"

    @commands.group()
    async def mama(self, ctx):
        pass

    @mama.command(aliases=["top"])
    async def top1(self, ctx):
        url = f"{self.base_url}/rankingDetailData.json"
        params = query_string_from_dict(
            dict(
                sectionID=0,
                type="top1",
            )
        )
        endpoint = f"{url}?{params}"

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as res:
                if res.status != 200:
                    raise ConnectionError
                else:
                    top = await res.read()
                    top = top.decode("utf-8")
                    top = json.loads(top)["rankList"]

        base_url = f"{self.base_url}/totalVoteCnt.json"

        async with aiohttp.ClientSession() as session:
            async with session.get(base_url) as res:
                if res.status != 200:
                    raise ConnectionError
                else:
                    total = await res.read()
                    total = total.decode("utf-8")
                    total = json.loads(total)

        embed = discord.Embed(
            title="MAMA 2021 Current Voting Results",
            url=f"{self.base_url}/ranking",
            color=discord.Color.gold(),
            description=f'Total number of votes: **{total["data"]["totalVoteCnt"]:,d}**',
        )
        embed.add_field(
            name=f'{top[0]["SECTION_NAME_M_BRR_ENG"]}',
            value=f'**{top[0]["ARTIST_NAME_ENG"]}** ({top[0]["CANDIDATE_VOTE_PERCENT"]}%)',
            inline=True,
        )
        embed.add_field(
            name=f'{top[1]["SECTION_NAME_M_BRR_ENG"]}',
            value=f'**{top[1]["ARTIST_NAME_ENG"]} - {top[1]["SONG_NAME_ENG"]}** ({top[1]["CANDIDATE_VOTE_PERCENT"]}%)',
            inline=True,
        )
        embed.add_field(
            name=f'{top[2]["SECTION_NAME_M_BRR_ENG"]}',
            value=f'**{top[2]["ARTIST_NAME_ENG"]}** '
            + f'[{top[2]["HASH_TAG_NAME"]}](https://twitter.com/hashtag/{top[2]["HASH_TAG_NAME"][1:]}) '
            + f'({top[2]["CANDIDATE_VOTE_PERCENT"]}%)',
            inline=False,
        )
        for category in top[3:9]:
            embed.add_field(
                name=f'{category["SECTION_NAME_M_BRR_ENG"].replace("<br/>", " ")}',
                value=f'**{category["ARTIST_NAME_ENG"]}** ({category["CANDIDATE_VOTE_PERCENT"]}%)',
                inline=False,
            )
        for category in top[9:]:
            embed.add_field(
                name=f'{category["SECTION_NAME_M_BRR_ENG"].replace("<br/>", " ")}',
                value=f'**{category["ARTIST_NAME_ENG"]} - '
                + f'{category["SONG_NAME_ENG"]}** '
                + f'({category["CANDIDATE_VOTE_PERCENT"]}%)',
                inline=False,
            )
        embed.set_footer(text=f'Last update: {total["data"]["currentTime"]} (KST)')

        await ctx.send(embed=embed)

    @mama.command(aliases=["aoty", "artist-of-the-year"])
    async def album_of_the_year(self, ctx):
        url = f"{self.base_url}/rankingDetailData.json"
        params = query_string_from_dict(dict(sectionID=1))
        endpoint = f"{url}?{params}"

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as res:
                if res.status != 200:
                    raise ConnectionError
                else:
                    aoty = await res.read()
                    aoty = aoty.decode("utf-8")
                    aoty = json.loads(aoty)

        embed = discord.Embed(
            title="MAMA 2021 Current Voting Results - Artist of the Year",
            url=f"{self.base_url}/rankingDetail?sectionID=1",
            color=discord.Color.gold(),
            description=f'Total number of votes: **{aoty["sectionVoteSum"]:,d}**',
        )
        for i, artist in enumerate(aoty["rankList"]):
            embed.add_field(
                name=f'{i+1}. {artist["ARTIST_NAME_ENG"]}',
                value=f'{artist["CANDIDATE_VOTE_PERCENT"]}%',
                inline=True,
            )

        await ctx.send(embed=embed)

    @mama.command(aliases=["soty", "song-of-the-year"])
    async def song_of_the_year(self, ctx):
        url = f"{self.base_url}/rankingDetailData.json"
        params = query_string_from_dict(dict(sectionID=2))
        endpoint = f"{url}?{params}"

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as res:
                if res.status != 200:
                    raise ConnectionError
                else:
                    soty = await res.read()
                    soty = soty.decode("utf-8")
                    soty = json.loads(soty)

        embed = discord.Embed(
            title="MAMA 2021 Current Voting Results - Song of the Year",
            url=f"{self.base_url}/rankingDetail?sectionID=2",
            color=discord.Color.gold(),
            description=f'Total number of votes: **{soty["sectionVoteSum"]:,d}**',
        )
        for i, artist in enumerate(soty["rankList"]):
            embed.add_field(
                name=f'{i + 1}. {artist["ARTIST_NAME_ENG"]}',
                value=f'**{artist["SONG_NAME_ENG"]}** ({artist["CANDIDATE_VOTE_PERCENT"]}%)',
                inline=True,
            )

        await ctx.send(embed=embed)

    @mama.command(aliases=["worldwide", "worldwide-fans-choice"])
    async def worldwide_fans_choice(self, ctx):
        url = f"{self.base_url}/rankingDetailData.json"
        params = query_string_from_dict(dict(sectionID=3))
        endpoint = f"{url}?{params}"

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as res:
                if res.status != 200:
                    raise ConnectionError
                else:
                    worldwide = await res.read()
                    worldwide = worldwide.decode("utf-8")
                    worldwide = json.loads(worldwide)

        embed = discord.Embed(
            title="MAMA 2021 Current Voting Results - Worldwide Fans' Choice Top 10",
            url=f"{self.base_url}/rankingDetail?sectionID=2",
            color=discord.Color.gold(),
            description=f'Total number of votes: **{worldwide["sectionVoteSum"]:,d}**',
        )
        for i, artist in enumerate(worldwide["rankList"]):
            embed.add_field(
                name=f'{i + 1}. {artist["ARTIST_NAME_ENG"]}',
                value=f'{artist["CANDIDATE_VOTE_PERCENT"]}%',
                inline=True,
            )

        await ctx.send(embed=embed)


def setup(client):
    # client.add_cog(Mama2021(client))
    pass
