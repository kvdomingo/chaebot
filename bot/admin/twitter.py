from django.contrib import admin

from ..models import TwitterMediaSource, TwitterMediaSubscribedChannel


class TwitterMediaSourceInline(admin.TabularInline):
    model = TwitterMediaSource


class TwitterMediaSubscribedChannelInline(admin.TabularInline):
    model = TwitterMediaSubscribedChannel
