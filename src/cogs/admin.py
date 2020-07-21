import os
from datetime import datetime, timedelta
from discord.ext import commands
from src.crud import *


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(hidden=True)
    async def admin(self, ctx):
        if str(ctx.message.author) != os.environ['DISCORD_ADMIN']:
            ctx.send('Sorry, you are not authorized to access that command.')
            return
        else:
            pass

    @admin.command(aliases=['status'], help='Get technical bot status', hidden=True)
    async def admin_status(self, ctx):
        created = os.environ['HEROKU_RELEASE_CREATED_AT']
        created = datetime.strptime(created, '%Y-%m-%dT%H:%M:%SZ')
        created += timedelta(hours=8)
        message = f"""
        ```
        Latest release:
            {os.environ['HEROKU_RELEASE_VERSION']}
            {os.environ['HEROKU_SLUG_DESCRIPTION']}
            {created}
        ```
        """
        await ctx.send(message)

    @admin.group(aliases=['group'], hidden=True)
    async def admin_group(self, ctx):
        pass

    @admin_group.command(aliases=['get', 'read'], hidden=True)
    async def group_get(self, ctx, name=None):
        response = GroupApi().get(name)
        await ctx.send(response)

    @admin_group.command(aliases=['add', 'create'], hidden=True)
    async def group_add(self, ctx, name, vlive_channel_code=None, vlive_channel_seq=None, vlive_last_seq=None):
        kwargs = {k: v for k, v in list(locals().items())[2:]}
        message = GroupApi().create(**kwargs)
        await ctx.send(message)

    @admin_group.command(aliases=['edit', 'update'], hidden=True)
    async def group_edit(self, ctx, old_name, new_name):
        message = GroupApi().update(old_name, new_name)
        await ctx.send(message)

    @admin.group(aliases=['member'], hidden=True)
    async def admin_member(self, ctx):
        pass

    @admin_member.command(aliases=['get', 'read'], hidden=True)
    async def member_get(self, ctx, group, name):
        message = MemberApi().get(group, name)
        await ctx.send(message)

    @admin_member.command(aliases=['add', 'create'], hidden=True)
    async def member_add(self, ctx, group, stage_name, family_name, given_name):
        kwargs = {k: v for k, v in list(locals().items())[2:]}
        message = MemberApi().create(**kwargs)
        await ctx.send(message)

    @admin.group(aliases=['account'], hidden=True)
    async def admin_account(self, ctx):
        pass

    @admin_account.command(aliases=['get'], hidden=True)
    async def account_get(self, ctx, group, member):
        message = AccountApi().get(group, member)
        await ctx.send(message)

    @admin_account.command(aliases=['create', 'add'], hidden=True)
    async def account_add(self, ctx, group, member, account_name):
        kwargs = {k: v for k, v in list(locals().items())[2:]}
        message = AccountApi().create(**kwargs)
        await ctx.send(message)

    @admin_account.command(aliases=['update', 'edit'], hidden=True)
    async def account_edit(self, ctx, group, member, old_account, new_account):
        kwargs = {k: v for k, v in list(locals().items())[2:]}
        message = AccountApi().update(**kwargs)
        await ctx.send(message)

    @admin.group(aliases=['alias'], hidden=True)
    async def admin_alias(self, ctx):
        pass

    @admin_alias.command(aliases=['get'], hidden=True)
    async def alias_get(self, ctx, group, member):
        message = AliasApi().get(group, member)
        await ctx.send(message)

    @admin_alias.command(aliases=['add', 'create'], hidden=True)
    async def alias_add(self, ctx, group, member, alias):
        message = AliasApi().create(group, member, alias)
        await ctx.send(message)


def setup(client):
    client.add_cog(Admin(client))
