from rest_framework.serializers import ModelSerializer

from ..models import MemberAlias


class MemberAliasSerializer(ModelSerializer):
    class Meta:
        model = MemberAlias
        fields = "__all__"
