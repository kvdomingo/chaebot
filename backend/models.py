from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name.upper()


class Member(models.Model):
    stage_name = models.CharField(max_length=64)
    given_name = models.CharField(max_length=64)
    family_name = models.CharField(max_length=64)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.stage_name} of {str(self.group)}'


class Alias(models.Model):
    alias = models.CharField(max_length=64)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Aliases'

    def __str__(self):
        return f'{self.alias} ({self.member.stage_name} of {str(self.member.group)})'


class TwitterAccount(models.Model):
    account_name = models.CharField(max_length=255)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.account_name} (for {str(self.member)})'


class Channel(models.Model):
    channel_id = models.BigIntegerField(unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.channel_id} ({str(self.group)})'
