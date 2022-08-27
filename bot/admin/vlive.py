from django.contrib import admin

from ..models import VliveSubscribedChannel


class VliveSubscribedChannelInline(admin.TabularInline):
    model = VliveSubscribedChannel


class VliveSubscribedChannelAdmin(admin.ModelAdmin):
    list_display = ["channel_id", "group"]
