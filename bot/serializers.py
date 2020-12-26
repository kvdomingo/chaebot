from rest_framework import serializers
from .models import *


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupAlias
        fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):
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
