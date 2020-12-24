from django.contrib import admin
from .models import *


admin.site.register(Group)
admin.site.register(GroupAlias)
admin.site.register(Member)
admin.site.register(MemberAlias)
admin.site.register(TwitterMediaSource)
admin.site.register(TwitterMediaSubscribedChannel)
admin.site.register(VliveSubscribedChannel)

admin.site.index_title = 'Admin'
admin.site.site_title = 'kvisualbot'
admin.site.site_header = 'kvisualbot administration'
