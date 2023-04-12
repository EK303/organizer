from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from django.db.models import Q

from main.models import Column, Board

from main.serializers.cards import CardListSerializer


class ColumnSerializer(serializers.Serializer):
    title = serializers.CharField()
    id = serializers.IntegerField()
    cards = CardListSerializer(many=True)


class ColumnCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    board_id = serializers.IntegerField(required=True)

    def validate(self, attrs):
        if Column.objects.filter(Q(title=attrs['title']) & Q(board_id=attrs['board_id'])).exists():
            return Response(f"A column with name {attrs['title']} already exists", status=status.HTTP_409_CONFLICT)
        return attrs

    def create(self, validated_data):
        return Column.objects.create(title=validated_data.get("title"),
                                     board_id=validated_data.get("board_id"))


class ColumnEditSerializer(serializers.Serializer):

    title = serializers.CharField()
    board_id = serializers.IntegerField()

    def validate(self, attrs):
        if attrs['board_id'] == 0:
            return Response("Invalid board parameter", status=status.HTTP_400_BAD_REQUEST)
        if not Board.objects.filter(pk=attrs['board_id']).exists():
            raise NotFound("Board not found")
        if Board.objects.filter(Q(title=attrs['title']) & Q(pk=attrs['board_id'])).exists():
            raise serializers.ValidationError("A column with this title already exists in this board")
        return attrs

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title")
        instance.board_id = validated_data.get("board_id")
        instance.save()
        return instance

