from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import VliveSubscribedChannel
from ..serializers import VliveSubscribedChannelSerializer


class VliveSubscribedChannelView(APIView):
    def get(self, request, channel_id=None):
        if channel_id is None:
            query = VliveSubscribedChannel.objects.all()
        else:
            query = VliveSubscribedChannel.objects.filter(channel_id=channel_id).all()
        serializer = VliveSubscribedChannelSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VliveSubscribedChannelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
