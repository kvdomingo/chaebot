from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Group
from ..serializers import (
    GroupAliasSerializer,
    GroupSerializer,
    MemberSerializer,
    TwitterMediaSubscribedChannelSerializer,
)


class GroupView(APIView):
    queryset = Group.objects.prefetch_related(
        "aliases",
        "members",
        "members__twitter_media_sources",
        "members__aliases",
        "twitter_media_subscribed_channels",
    ).all()

    def get(self, request, pk=None):
        if pk is None:
            many = True
            query = self.queryset.all().order_by("name")
        else:
            many = False
            query = self.queryset.get(pk=pk)
        serializer = GroupSerializer(query, many=many)
        return Response(serializer.data)

    def patch(self, request, pk):
        group = self.queryset.get(pk=pk)
        serializer = GroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupAliasView(APIView):
    queryset = Group.objects.prefetch_related("aliases").all()

    def get(self, request, pk=None):
        query = self.queryset.get(pk=pk).aliases.all()
        serializer = GroupAliasSerializer(query, many=True)
        return Response(serializer.data)


class GroupMembersView(APIView):
    queryset = Group.objects.prefetch_related(
        "members", "members__twitter_media_sources", "members__aliases"
    ).all()

    def get(self, request, pk):
        query = self.queryset.get(pk=pk).members.all()
        serializer = MemberSerializer(query, many=True)
        return Response(serializer.data)


class GroupTwitterSubscribedChannelsView(APIView):
    queryset = Group.objects.prefetch_related("twitter_media_subscribed_channels").all()

    def get(self, request, pk):
        query = self.queryset.get(pk=pk).twitter_media_subscribed_channels.all()
        serializer = TwitterMediaSubscribedChannelSerializer(query, many=True)
        return Response(serializer.data)
