from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


class GroupApi(APIView):
    def get(self, request, pk=None):
        if pk is None:
            many = True
            query = Group.objects.all().order_by("name")
        else:
            many = False
            query = Group.objects.get(pk=pk)
        serializer = GroupSerializer(query, many=many)
        return Response(serializer.data)

    def patch(self, request, pk):
        group = Group.objects.get(pk=pk)
        serializer = GroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupAliasApi(APIView):
    def get(self, request, pk=None):
        query = Group.objects.get(pk=pk).aliases.all()
        serializer = GroupAliasSerializer(query, many=True)
        return Response(serializer.data)


class GroupMembersApi(APIView):
    def get(self, request, pk):
        query = Group.objects.get(pk=pk).members.all()
        serializer = MemberSerializer(query, many=True)
        return Response(serializer.data)


class GroupTwitterSubscribedChannelsApi(APIView):
    def get(self, request, pk):
        query = Group.objects.get(pk=pk).twitter_media_subscribed_channels.all()
        serializer = TwitterMediaSubscribedChannelSerializer(query, many=True)
        return Response(serializer.data)


class GroupVliveSubscribedChannelsApi(APIView):
    def get(self, request, pk):
        query = Group.objects.get(pk=pk).vlive_subscribed_channels.all()
        serializer = VliveSubscribedChannelSerializer(query, many=True)
        return Response(serializer.data)


class MemberApi(APIView):
    def get(self, request, pk=None):
        if pk is None:
            many = True
            query = Member.objects.all()
        else:
            many = False
            query = Member.objects.get(pk=pk)
        serializer = MemberSerializer(query, many=many)
        return Response(serializer.data)


class MemberAliasApi(APIView):
    def get(self, request, pk):
        query = Member.objects.get(pk=pk).aliases.all()
        serializer = MemberAliasSerializer(query, many=True)
        return Response(serializer.data)


class MemberTwitterMediaSourceApi(APIView):
    def get(self, request, pk):
        query = Member.objects.get(pk=pk).twitter_media_sources.all()
        serializer = TwitterMediaSourceSerializer(query, many=True)
        return Response(serializer.data)


class TwitterMediaSourceApi(APIView):
    def get(self, request, pk=None):
        if pk is None:
            many = True
            query = TwitterMediaSource.objects.all()
        else:
            many = False
            query = TwitterMediaSource.objects.get(pk=pk)
        serializer = TwitterMediaSourceSerializer(query, many=many)
        return Response(serializer.data)


class TwitterMediaSubscribedChannelApi(APIView):
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


class VliveSubscribedChannelApi(APIView):
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
