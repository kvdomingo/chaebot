from django.contrib import admin

from ..models import Group, Member, ScheduleSubscriber, TwitterMediaSubscribedChannel
from .group import GroupAdmin, GroupAliasInline
from .member import MemberAdmin, MemberAliasInline, MemberInline
from .twitter import TwitterMediaSourceInline, TwitterMediaSubscribedChannelInline

admin.site.register(Group, GroupAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(ScheduleSubscriber)
admin.site.register(TwitterMediaSubscribedChannel)

admin.site.index_title = "Admin"
admin.site.site_title = "ChaeBot"
admin.site.site_header = "ChaeBot Administration"
