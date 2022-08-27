from django.db import models


class Member(models.Model):
    stage_name = models.CharField(max_length=16)
    given_name = models.CharField(max_length=16)
    family_name = models.CharField(max_length=16)
    # korean_name = models.CharField(max_length=32, blank=True, null=True)
    # chinese_name = models.CharField(max_length=32, blank=True, null=True)
    english_name = models.CharField(max_length=32, blank=True, null=True)
    # native_name = models.CharField(max_length=32, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    group = models.ForeignKey("Group", related_name="members", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.stage_name} ({self.group.name})"

    class Meta:
        ordering = ["group__name", "birthday", "stage_name"]


class MemberAlias(models.Model):
    alias = models.CharField(max_length=32)
    member = models.ForeignKey("Member", related_name="aliases", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.alias} ({self.member.stage_name} of {self.member.group.name})"

    class Meta:
        verbose_name_plural = "member aliases"
        ordering = ["member__group__name", "member__stage_name", "alias"]
