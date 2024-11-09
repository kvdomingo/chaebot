from rest_framework import serializers

from bot.models import Comeback


class ComebackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comeback
        fields = "__all__"
