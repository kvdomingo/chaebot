from django.contrib import admin
from .models import *


class MemberInline(admin.TabularInline):
    model = Member


class ChannelInline(admin.TabularInline):
    model = Channel


class AliasInline(admin.TabularInline):
    model = Alias


class TwitterAccountInline(admin.TabularInline):
    model = TwitterAccount


class GroupAdmin(admin.ModelAdmin):
    inlines = [MemberInline, ChannelInline]


class MemberAdmin(admin.ModelAdmin):
    inlines = [AliasInline, TwitterAccountInline]


admin.site.register(Group, GroupAdmin)
admin.site.register(Member, MemberAdmin)
