from rest_framework.serializers import ModelSerializer

from ..models import GroupAlias


class GroupAliasSerializer(ModelSerializer):
    class Meta:
        model = GroupAlias
        fields = "__all__"
