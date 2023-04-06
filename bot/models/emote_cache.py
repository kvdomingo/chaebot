from datetime import datetime
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db import models


def timestamp_factory():
    return datetime.now(ZoneInfo(settings.TIME_ZONE))


class MediaCache(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True, unique=True, db_index=True)
    guild_id = models.PositiveBigIntegerField(unique=True, db_index=True)
    channel_id = models.PositiveBigIntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=64)
    url = models.URLField()

    class Meta:
        ordering = ["id"]
        abstract = True

    def __str__(self):
        return f"[{self.id}] {self.name}"


class UserCache(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True, unique=True, db_index=True)
    name = models.CharField(max_length=64)
    discriminator = models.CharField(max_length=8)
    avatar = models.URLField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}#{self.discriminator}"


class MediaUsage(models.Model):
    timestamp = models.DateTimeField(default=timestamp_factory)

    class Meta:
        ordering = ["-timestamp"]
        abstract = True


class StickerCache(MediaCache):
    @property
    def usage_count(self):
        return self.usage.count()


class EmoteCache(MediaCache):
    @property
    def usage_count(self):
        return self.usage.count()


class StickerUsage(MediaUsage):
    sticker = models.ForeignKey(StickerCache, on_delete=models.CASCADE, related_name="usage")
    user = models.ForeignKey(UserCache, on_delete=models.SET_NULL, null=True, blank=True, related_name="sticker_usage")

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f%z')}] {self.sticker.name} by {self.user}"


class EmoteUsage(MediaUsage):
    emote = models.ForeignKey(EmoteCache, on_delete=models.CASCADE, related_name="usage")
    user = models.ForeignKey(UserCache, on_delete=models.SET_NULL, null=True, blank=True, related_name="emote_usage")

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f%z')}] {self.emote.name} by {self.user}"
