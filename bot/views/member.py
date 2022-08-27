from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Member
from ..serializers import MemberAliasSerializer, MemberSerializer, TwitterMediaSourceSerializer


class MemberView(APIView):
    def get(self, request, pk=None):
        if pk is None:
            many = True
            query = Member.objects.all()
        else:
            many = False
            query = Member.objects.get(pk=pk)
        serializer = MemberSerializer(query, many=many)
        return Response(serializer.data)


class MemberAliasView(APIView):
    def get(self, request, pk):
        query = Member.objects.get(pk=pk).aliases.all()
        serializer = MemberAliasSerializer(query, many=True)
        return Response(serializer.data)


class MemberTwitterMediaSourceView(APIView):
    def get(self, request, pk):
        query = Member.objects.get(pk=pk).twitter_media_sources.all()
        serializer = TwitterMediaSourceSerializer(query, many=True)
        return Response(serializer.data)
