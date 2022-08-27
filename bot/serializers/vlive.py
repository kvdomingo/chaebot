from rest_framework.serializers import ModelSerializer

from ..models import VliveSubscribedChannel


class VliveSubscribedChannelSerializer(ModelSerializer):
    class Meta:
        model = VliveSubscribedChannel
        fields = "__all__"
