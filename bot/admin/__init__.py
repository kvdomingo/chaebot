from django.contrib import admin

from ..models import Group, Member, TwitterMediaSubscribedChannel, VliveSubscribedChannel
from .group import GroupAdmin, GroupAliasInline
from .member import MemberAdmin, MemberAliasInline, MemberInline
from .twitter import TwitterMediaSourceInline, TwitterMediaSubscribedChannelInline
from .vlive import VliveSubscribedChannelAdmin, VliveSubscribedChannelInline

# admin.site.register(GroupAlias)
# admin.site.register(MemberAlias)
# admin.site.register(TwitterMediaSource)
admin.site.register(Group, GroupAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(VliveSubscribedChannel, VliveSubscribedChannelAdmin)
admin.site.register(TwitterMediaSubscribedChannel)

admin.site.index_title = "Admin"
admin.site.site_title = "kvisualbot"
admin.site.site_header = "kvisualbot administration"
