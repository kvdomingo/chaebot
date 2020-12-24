from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=16, unique=True)
    vlive_channel_code = models.CharField(max_length=32)
    vlive_channel_seq = models.BigIntegerField()
    vlive_last_seq = models.BigIntegerField()
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
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

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
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.account_name} (for {self.member.stage_name} of {self.member.group.name})'


class TwitterMediaSubscribedChannel(models.Model):
    channel_id = models.BigIntegerField(unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.channel_id} ({self.group.name})'


class VliveSubscribedChannel(models.Model):
    channel_id = models.BigIntegerField(unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.channel_id} ({self.group.name})'
