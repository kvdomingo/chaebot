from rest_framework import serializers

from ..models import ScheduleSubscriber


class ScheduleSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleSubscriber
        fields = "__all__"
