from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from ..models import ScheduleSubscriber
from ..serializers import ScheduleSubscriberSerializer


class ScheduleSubscriberView(ModelViewSet):
    queryset = ScheduleSubscriber.objects.all()
    serializer_class = ScheduleSubscriberSerializer


class ScheduleSubscriberFromGuildView(RetrieveModelMixin, GenericViewSet):
    queryset = ScheduleSubscriber.objects.all()
    serializer_class = ScheduleSubscriberSerializer

    def retrieve(self, request, *args, **kwargs):
        guild_id = kwargs.get("pk")
        queryset = self.queryset.all().get(guild_id=guild_id)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)
