from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ..models import Group
from .group_alias import GroupAliasSerializer
from .member import MemberSerializer
from .twitter import TwitterMediaSubscribedChannelSerializer


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

    aliases = SerializerMethodField()
    members = SerializerMethodField()
    twitterMediaSubscribedChannels = SerializerMethodField()

    def get_aliases(self, obj: Meta.model):
        aliases = obj.aliases.all()
        serializer = GroupAliasSerializer(aliases, many=True)
        return serializer.data

    def get_members(self, obj: Meta.model):
        members = obj.members.all()
        serializer = MemberSerializer(members, many=True)
        return serializer.data

    def get_twitterMediaSubscribedChannels(self, obj: Meta.model):
        channels = obj.twitter_media_subscribed_channels.all()
        serializer = TwitterMediaSubscribedChannelSerializer(channels, many=True)
        return serializer.data
