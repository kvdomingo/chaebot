import os
from datetime import datetime, timedelta

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context
from django.conf import settings

from kvisualbot.logging import logger


class Admin(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client
        self.time_up = datetime.now()

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Logged in as {self.client.user}")
        if settings.PYTHON_ENV != "production":
            activity_name = "under development"
            status = discord.Status.do_not_disturb
        else:
            activity_name = f"in {len(self.client.guilds)} servers!"
            status = discord.Status.online
        await self.client.change_presence(
            status=status,
            activity=discord.Game(name=activity_name),
        )

    @commands.group(hidden=True)
    async def admin(self, ctx):
        if str(ctx.message.author.id) != os.environ.get("DISCORD_ADMIN_ID"):
            embed = discord.Embed(
                description="Sorry, you do not have sufficient permissions to use `admin` commands.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return
        else:
            pass

    @admin.command(aliases=["status", "meta"], help="Get technical bot status", hidden=True)
    async def admin_status(self, ctx: Context):
        created = os.environ["HEROKU_RELEASE_CREATED_AT"]
        created = datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ")
        created += timedelta(hours=8)
        time_now = datetime.now()
        uptime = str(time_now - self.time_up)
        embed = discord.Embed(
            title="Latest release",
            color=discord.Color.green(),
        )
        embed.add_field(
            name="Version",
            value=os.environ.get("HEROKU_RELEASE_VERSION"),
            inline=False,
        )
        embed.add_field(
            name="Hash",
            value=os.environ.get("HEROKU_SLUG_DESCRIPTION"),
            inline=False,
        )
        embed.add_field(
            name="Build time",
            value=str(created),
            inline=False,
        )
        embed.add_field(
            name="Uptime",
            value=str(uptime),
            inline=False,
        )
        await ctx.send(embed=embed)


async def setup(client: Bot):
    await client.add_cog(Admin(client))
