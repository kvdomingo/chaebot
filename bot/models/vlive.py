from django.db import models


class VliveSubscribedChannel(models.Model):
    channel_id = models.BigIntegerField()
    group = models.ForeignKey("Group", related_name="vlive_subscribed_channels", on_delete=models.CASCADE)
    dev_channel = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.channel_id} ({self.group.name})"

    class Meta:
        ordering = ["group__name", "channel_id"]
        unique_together = ["channel_id", "group"]
