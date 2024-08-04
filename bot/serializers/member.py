from rest_framework.serializers import ModelSerializer, SerializerMethodField

from bot.models import Member

from .member_alias import MemberAliasSerializer
from .twitter import TwitterMediaSourceSerializer


class MemberSerializer(ModelSerializer):
    aliases = SerializerMethodField()
    twitterMediaSources = SerializerMethodField()

    def get_aliases(self, obj):
        aliases = obj.aliases.all()
        serializer = MemberAliasSerializer(aliases, many=True)
        return serializer.data

    def get_twitterMediaSources(self, obj):
        sources = obj.twitter_media_sources.all()
        serializer = TwitterMediaSourceSerializer(sources, many=True)
        return serializer.data

    class Meta:
        model = Member
        fields = "__all__"
