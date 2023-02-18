from django.db import models


class ScheduleSubscriber(models.Model):
    guild_id = models.BigIntegerField()
    channel_id = models.BigIntegerField()
    message_id = models.BigIntegerField(blank=True, null=True, unique=True, db_index=True)

    def __str__(self):
        return f"{self.guild_id} - {self.channel_id} - {self.message_id}"

    class Meta:
        unique_together = ["guild_id", "channel_id", "message_id"]
