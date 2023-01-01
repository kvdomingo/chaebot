from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=32, unique=True)
    twitter_user_name = models.CharField(max_length=16, blank=True)
    instagram_user_name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]


class GroupAlias(models.Model):
    alias = models.CharField(max_length=16, unique=True)
    group = models.ForeignKey("Group", related_name="aliases", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.alias} ({self.group.name})"

    class Meta:
        verbose_name_plural = "group aliases"
        ordering = ["group__name", "alias"]
