from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Group
from ..serializers import (
    GroupAliasSerializer,
    GroupSerializer,
    MemberSerializer,
    TwitterMediaSubscribedChannelSerializer,
    VliveSubscribedChannelSerializer,
)


class GroupView(APIView):
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


class GroupAliasView(APIView):
    def get(self, request, pk=None):
        query = Group.objects.get(pk=pk).aliases.all()
        serializer = GroupAliasSerializer(query, many=True)
        return Response(serializer.data)


class GroupMembersView(APIView):
    def get(self, request, pk):
        query = Group.objects.get(pk=pk).members.all()
        serializer = MemberSerializer(query, many=True)
        return Response(serializer.data)


class GroupTwitterSubscribedChannelsView(APIView):
    def get(self, request, pk):
        query = Group.objects.get(pk=pk).twitter_media_subscribed_channels.all()
        serializer = TwitterMediaSubscribedChannelSerializer(query, many=True)
        return Response(serializer.data)


class GroupVliveSubscribedChannelsView(APIView):
    def get(self, request, pk):
        query = Group.objects.get(pk=pk).vlive_subscribed_channels.all()
        serializer = VliveSubscribedChannelSerializer(query, many=True)
        return Response(serializer.data)
