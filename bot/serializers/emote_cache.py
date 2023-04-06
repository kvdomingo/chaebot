from rest_framework import serializers

from ..models import EmoteCache, EmoteUsage, StickerCache, StickerUsage, UserCache


class UserCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCache
        fields = "__all__"


class EmoteCacheSerializer(serializers.ModelSerializer):
    count = serializers.ReadOnlyField(source="usage_count")

    class Meta:
        model = EmoteCache
        fields = "__all__"


class EmoteUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmoteUsage
        fields = "__all__"


class StickerCacheSerializer(serializers.ModelSerializer):
    count = serializers.ReadOnlyField(source="usage_count")

    class Meta:
        model = StickerCache
        fields = "__all__"


class StickerUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StickerUsage
        fields = "__all__"
