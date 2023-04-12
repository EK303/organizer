from django.db.models import Q

from rest_framework import serializers, status
from rest_framework.response import Response

from users.serializers import UserSerializer

from main.models import Mark

from .services import is_hex_color


class BoardMarkSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class MarkListSerializer(serializers.Serializer):
    title = serializers.CharField()
    colour = serializers.CharField(required=False)
    id = serializers.IntegerField(read_only=True)


class MarkCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    colour = serializers.CharField(required=False)
    board_id = serializers.IntegerField(required=True)

    def validate(self, attrs):
        if Mark.objects.filter(Q(title=attrs['title']) & Q(board_id=attrs['board_id'])).exists():
            raise serializers.ValidationError("A mark with title already exists in this board")
        if not is_hex_color(attrs["colour"]):
            return Response("Invalid colour format", status=status.HTTP_400_BAD_REQUEST)
        return attrs

    def create(self, validated_data):
        return Mark.objects.create(title=validated_data.get("title"),
                                   colour=validated_data.get("colour"),
                                   board_id=validated_data.get("board_id"))

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title")
        instance.colour = validated_data.get("colour")
        instance.board_id = validated_data.get("board_id")
        instance.save()
        return instance
