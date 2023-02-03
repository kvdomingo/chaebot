from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import TwitterMediaSource, TwitterMediaSubscribedChannel
from ..serializers import (
    TwitterMediaSourceSerializer,
    TwitterMediaSubscribedChannelSerializer,
)


class TwitterMediaSourceView(APIView):
    def get(self, request, pk=None):
        if pk is None:
            many = True
            query = TwitterMediaSource.objects.all()
        else:
            many = False
            query = TwitterMediaSource.objects.get(pk=pk)
        serializer = TwitterMediaSourceSerializer(query, many=many)
        return Response(serializer.data)


class TwitterMediaSubscribedChannelView(APIView):
    def get(self, request, pk=None):
        if pk is None:
            many = True
            query = TwitterMediaSubscribedChannel.objects.all()
        else:
            many = False
            query = TwitterMediaSubscribedChannel.objects.get(pk=pk)
        serializer = TwitterMediaSubscribedChannelSerializer(query, many=many)
        return Response(serializer.data)

    def post(self, request):
        serializer = TwitterMediaSubscribedChannelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        channel = TwitterMediaSubscribedChannel.objects.get(pk=pk)
        channel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
