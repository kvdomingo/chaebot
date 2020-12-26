from django.db import models
from django.db.models import CharField
from django.db.models.functions import Lower


CharField.register_lookup(Lower)


class Group(models.Model):
    name = models.CharField(max_length=32, unique=True)
    vlive_channel_code = models.CharField(max_length=32, null=True)
    vlive_channel_seq = models.BigIntegerField(null=True)
    vlive_last_seq = models.BigIntegerField(null=True)
    twitter_user_name = models.CharField(max_length=16, blank=True)
    instagram_user_name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class GroupAlias(models.Model):
    alias = models.CharField(max_length=16, unique=True)
    group = models.ForeignKey(Group, related_name='aliases', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.alias} ({self.group.name})'

    class Meta:
        verbose_name_plural = 'group aliases'
        ordering = ['group__name', 'alias']


class Member(models.Model):
    stage_name = models.CharField(max_length=16)
    given_name = models.CharField(max_length=16)
    family_name = models.CharField(max_length=16)
    english_name = models.CharField(max_length=16, null=True)
    birthday = models.DateField(blank=True, null=True)
    group = models.ForeignKey(Group, related_name='members', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.stage_name} ({self.group.name})'

    class Meta:
        ordering = ['group__name', 'stage_name']


class MemberAlias(models.Model):
    alias = models.CharField(max_length=32)
    member = models.ForeignKey(Member, related_name='aliases', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.alias} ({self.member.stage_name} of {self.member.group.name})'

    class Meta:
        verbose_name_plural = 'member aliases'
        ordering = ['member__group__name', 'member__stage_name', 'alias']


class TwitterMediaSource(models.Model):
    account_name = models.CharField(max_length=16, unique=True)
    member = models.ForeignKey(Member, related_name='twitter_media_sources', on_delete=models.CASCADE)
    last_tweet_id = models.BigIntegerField(null=True)

    def __str__(self):
        return f'{self.account_name} (for {self.member.stage_name} of {self.member.group.name})'


class TwitterMediaSubscribedChannel(models.Model):
    channel_id = models.BigIntegerField(unique=True)
    group = models.ForeignKey(Group, related_name='twitter_media_subscribed_channels', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.channel_id} ({self.group.name})'


class VliveSubscribedChannel(models.Model):
    channel_id = models.BigIntegerField(unique=True)
    group = models.ForeignKey(Group, related_name='vlive_subscribed_channels', on_delete=models.CASCADE)
    dev_channel = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.channel_id} ({self.group.name})'

    class Meta:
        ordering = ['group__name', 'channel_id']
