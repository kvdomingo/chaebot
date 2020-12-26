import random
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


class GroupApi(APIView):
    def get(self, request, group_query=None):
        if group_query is None:
            many = True
            query = Group.objects.all().order_by('name')
        else:
            many = False
            query = Group.objects.filter(name__unaccent__lower__trigram_similar=group_query.lower()).first()
            if not query:
                query = GroupAlias.objects.filter(alias__unaccent__lower__trigram_similar=group_query.lower()).first()
                query = query.group
            if not query:
                many = True
                query = random.choice(Group.objects.all())
        serializer = GroupSerializer(query, many=many)
        return Response(serializer.data)


class MemberApi(APIView):
    def get(self, request, member_query=None):
        if member_query is None:
            many = True
            query = Member.objects.all()
        else:
            many = False
            query = Member.objects.filter(stage_name__unaccent__lower__trigram_similar=member_query.lower()).first()
            if not query:
                query = Member.objects.filter(given_name__unaccent__lower__trigram_similar=member_query.lower()).first()
            if not query:
                query = Member.objects.filter(family_name__unaccent__lower__trigram_similar=member_query.lower()).first()
            if not query:
                query = MemberAlias.objects.filter(alias__unaccent__lower__trigram_similar=member_query.lower()).first()
            if not query:
                many = True
                query = random.choice(Member.objects.all())
        serializer = MemberSerializer(query, many=many)
        return Response(serializer.data)
