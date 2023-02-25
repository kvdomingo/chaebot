from django.db import models


class ScheduleSubscriber(models.Model):
    guild_id = models.BigIntegerField(unique=True, db_index=True)
    channel_id = models.BigIntegerField()
    message_id = models.BigIntegerField(blank=True, null=True, unique=True, db_index=True)

    def __str__(self):
        return f"{self.guild_id} - {self.channel_id} - {self.message_id}"
