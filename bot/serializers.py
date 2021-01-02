from rest_framework import serializers
from .models import *


class GroupSerializer(serializers.ModelSerializer):
    aliases = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    twitterMediaSubscribedChannels = serializers.SerializerMethodField()
    vliveSubscribedChannels = serializers.SerializerMethodField()

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
        fields = '__all__'


class GroupAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupAlias
        fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):
    aliases = serializers.SerializerMethodField()
    twitterMediaSources = serializers.SerializerMethodField()

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
        fields = '__all__'


class MemberAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberAlias
        fields = '__all__'


class TwitterMediaSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterMediaSource
        fields = '__all__'


class TwitterMediaSubscribedChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterMediaSubscribedChannel
        fields = '__all__'


class VliveSubscribedChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VliveSubscribedChannel
        fields = '__all__'
