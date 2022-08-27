from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ..models import Group
from .group_alias import GroupAliasSerializer
from .member import MemberSerializer
from .twitter import TwitterMediaSubscribedChannelSerializer
from .vlive import VliveSubscribedChannelSerializer


class GroupSerializer(ModelSerializer):
    aliases = SerializerMethodField()
    members = SerializerMethodField()
    twitterMediaSubscribedChannels = SerializerMethodField()
    vliveSubscribedChannels = SerializerMethodField()

    def get_aliases(self, obj):
        aliases = obj.aliases.all()
        serializer = GroupAliasSerializer(aliases, many=True)
        return serializer.data

    def get_members(self, obj):
        members = obj.members.all()
        serializer = MemberSerializer(members, many=True)
        return serializer.data

    def get_twitterMediaSubscribedChannels(self, obj):
        channels = obj.twitter_media_subscribed_channels.all()
        serializer = TwitterMediaSubscribedChannelSerializer(channels, many=True)
        return serializer.data

    def get_vliveSubscribedChannels(self, obj):
        channels = obj.vlive_subscribed_channels.all()
        serializer = VliveSubscribedChannelSerializer(channels, many=True)
        return serializer.data

    class Meta:
        model = Group
        fields = "__all__"
