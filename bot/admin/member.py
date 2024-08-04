from django.contrib import admin

from bot.models import Member, MemberAlias

from .twitter import TwitterMediaSourceInline


class MemberInline(admin.TabularInline):
    model = Member


class MemberAliasInline(admin.TabularInline):
    model = MemberAlias


class MemberAdmin(admin.ModelAdmin):
    list_display = ["stage_name", "group", "birthday"]
    inlines = [MemberAliasInline, TwitterMediaSourceInline]
