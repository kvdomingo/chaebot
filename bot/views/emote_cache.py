from rest_framework.viewsets import ModelViewSet

from bot.models import EmoteCache, EmoteUsage, StickerCache, StickerUsage, UserCache
from bot.serializers import (
    EmoteCacheSerializer,
    EmoteUsageSerializer,
    StickerCacheSerializer,
    StickerUsageSerializer,
    UserCacheSerializer,
)


class UserCacheView(ModelViewSet):
    queryset = UserCache.objects.all()
    serializer_class = UserCacheSerializer


class EmoteCacheView(ModelViewSet):
    queryset = EmoteCache.objects.all()
    serializer_class = EmoteCacheSerializer


class EmoteUsageView(ModelViewSet):
    queryset = EmoteUsage.objects.all()
    serializer_class = EmoteUsageSerializer


class StickerCacheView(ModelViewSet):
    queryset = StickerCache.objects.all()
    serializer_class = StickerCacheSerializer


class StickerUsageView(ModelViewSet):
    queryset = StickerUsage.objects.all()
    serializer_class = StickerUsageSerializer
