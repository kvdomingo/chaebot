from discord import Color, Embed
from discord.ext import commands


class Convenience(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong ({round(self.client.latency * 1000)}ms)')

    @commands.command(aliases=['purge', 'sanitize'])
    async def clear(self, ctx, amount: int = 0):
        if amount < 1:
            await ctx.send('Please specify a positive number.')
        else:
            await ctx.channel.purge(limit=amount + 1)

    @commands.command()
    async def changelog(self, ctx):
        embed = Embed(
            title='Update v1.0 20210108',
            color=Color.green(),
        )
        embed.add_field(
            name='Commands changelog',
            value="""
            - All commands previously under the Query category should now be called behind !query or shorthand !q (e.g. before you would say !twice chaeyoung, now you need to say !q twice chaeyoung. Names don't have to be exact; aliases/common nicknames exist for each group/member name and will mostly match your target member given sensible aliases. For example, any of the following will give you TWICE's Chaeyoung: !q twice chae, !q twice chaeng, !q tdoong chaeng, !q teudoongie chaengie.
- !twitter commands have been renamed to !hourly
- Subscription commands now provide a list subcommand, e.g. to list all VLIVE subscriptions for a channel, say !vlive list. Similarly, to get all hourly subscriptions, say !hourly list. subscribe and unsubscribe subcommands should still work normally.
- !admin commands to get/create/edit/delete entries have been deprecated and can now only be done through the web interface. For now, the web interface has restricted access until I implement login via Discord OAuth. If you would like to request new groups, update member profiles, or add/edit aliases, feel free to drop them into #bot-support and tag me, or just DM me.
- For a complete list of commands, visit the documentation at https://kvisualbot.xyz/
            """,
            inline=False,
        )


def setup(client):
    client.add_cog(Convenience(client))
