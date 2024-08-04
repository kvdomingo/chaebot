from django.contrib import admin

from bot.models import GroupAlias

from .member import MemberInline
from .twitter import TwitterMediaSubscribedChannelInline


class GroupAliasInline(admin.TabularInline):
    model = GroupAlias


class GroupAdmin(admin.ModelAdmin):
    inlines = [GroupAliasInline, MemberInline, TwitterMediaSubscribedChannelInline]
