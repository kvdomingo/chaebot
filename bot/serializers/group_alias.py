from rest_framework.serializers import ModelSerializer

from bot.models import GroupAlias


class GroupAliasSerializer(ModelSerializer):
    class Meta:
        model = GroupAlias
        fields = "__all__"
