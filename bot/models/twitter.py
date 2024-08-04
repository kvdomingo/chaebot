from django.db import models


class TwitterMediaSource(models.Model):
    account_name = models.CharField(max_length=16, unique=True)
    member = models.ForeignKey(
        "Member", related_name="twitter_media_sources", on_delete=models.CASCADE
    )
    last_tweet_id = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.account_name} (for {self.member.stage_name} of {self.member.group.name})"


class TwitterMediaSubscribedChannel(models.Model):
    channel_id = models.BigIntegerField()
    group = models.ForeignKey(
        "Group",
        related_name="twitter_media_subscribed_channels",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.channel_id} ({self.group.name})"

    class Meta:
        unique_together = ["channel_id", "group"]
