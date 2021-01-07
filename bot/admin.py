from django.contrib import admin
from .models import *


class MemberInline(admin.TabularInline):
    model = Member


class MemberAliasInline(admin.TabularInline):
    model = MemberAlias


class GroupAliasInline(admin.TabularInline):
    model = GroupAlias


class VliveSubscribedChannelInline(admin.TabularInline):
    model = VliveSubscribedChannel


class TwitterMediaSourceInline(admin.TabularInline):
    model = TwitterMediaSource


class TwitterMediaSubscribedChannelInline(admin.TabularInline):
    model = TwitterMediaSubscribedChannel


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    inlines = [
        GroupAliasInline,
        MemberInline,
        VliveSubscribedChannelInline,
        TwitterMediaSubscribedChannelInline,
    ]


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['stage_name', 'group', 'birthday']
    inlines = [MemberAliasInline, TwitterMediaSourceInline]


# admin.site.register(GroupAlias)
# admin.site.register(MemberAlias)
# admin.site.register(TwitterMediaSource)
# admin.site.register(TwitterMediaSubscribedChannel)
# admin.site.register(VliveSubscribedChannel)

admin.site.index_title = 'Admin'
admin.site.site_title = 'kvisualbot'
admin.site.site_header = 'kvisualbot administration'
