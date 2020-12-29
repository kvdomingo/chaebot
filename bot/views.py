from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


class GroupApi(APIView):
    def get(self, request, pk=None):
        if pk is None:
            many = True
            query = Group.objects.all().order_by('name')
        else:
            many = False
            query = Group.objects.get(pk=pk)
        serializer = GroupSerializer(query, many=many)
        return Response(serializer.data)


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


class VliveSubscribedChannelApi(APIView):
    def get(self, request, pk=None):
        if pk is None:
            many = True
            query = VliveSubscribedChannel.objects.all()
        else:
            many = False
            query = VliveSubscribedChannel.objects.get(pk=pk)
        serializer = VliveSubscribedChannelSerializer(query, many=many)
        return Response(serializer.data)
