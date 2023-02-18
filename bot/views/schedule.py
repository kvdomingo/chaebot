from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import ScheduleSubscriber
from ..serializers import ScheduleSubscriberSerializer


class ScheduleSubscriberView(APIView):
    queryset = ScheduleSubscriber.objects.all()
    serializer_class = ScheduleSubscriberSerializer

    def get(self, request, pk=None):
        if pk is None:
            queryset = self.queryset.all()
        else:
            queryset = self.queryset.all().get(pk=pk)
        serializer = self.serializer_class(queryset, many=pk is None)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        queryset = self.queryset.all().get(pk=pk)
        serializer = self.serializer_class(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        queryset = self.queryset.all().get(pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ScheduleSubscriberFromGuildView(APIView):
    queryset = ScheduleSubscriber.objects.all()
    serializer_class = ScheduleSubscriberSerializer

    def get(self, request, guild_id):
        queryset = self.queryset.all().get(guild_id=guild_id)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)
