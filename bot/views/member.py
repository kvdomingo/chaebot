from rest_framework.response import Response
from rest_framework.views import APIView

from bot.models import Member
from bot.serializers import (
    MemberAliasSerializer,
    MemberSerializer,
    TwitterMediaSourceSerializer,
)


class MemberView(APIView):
    queryset = Member.objects.prefetch_related("aliases", "twitter_media_sources").all()

    def get(self, request, pk=None):
        if pk is None:
            many = True
            query = self.queryset.all()
        else:
            many = False
            query = self.queryset.get(pk=pk)
        serializer = MemberSerializer(query, many=many)
        return Response(serializer.data)


class MemberAliasView(APIView):
    queryset = Member.objects.prefetch_related("aliases").all()

    def get(self, request, pk):
        query = self.queryset.get(pk=pk).aliases.all()
        serializer = MemberAliasSerializer(query, many=True)
        return Response(serializer.data)


class MemberTwitterMediaSourceView(APIView):
    queryset = Member.objects.prefetch_related("twitter_media_sources").all()

    def get(self, request, pk):
        query = self.queryset.get(pk=pk).twitter_media_sources.all()
        serializer = TwitterMediaSourceSerializer(query, many=True)
        return Response(serializer.data)
