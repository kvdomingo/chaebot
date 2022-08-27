from rest_framework.serializers import ModelSerializer

from ..models import TwitterMediaSource, TwitterMediaSubscribedChannel


class TwitterMediaSourceSerializer(ModelSerializer):
    class Meta:
        model = TwitterMediaSource
        fields = "__all__"


class TwitterMediaSubscribedChannelSerializer(ModelSerializer):
    class Meta:
        model = TwitterMediaSubscribedChannel
        fields = "__all__"
