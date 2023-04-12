from django.db.models import Q

from rest_framework import serializers, status
from rest_framework.response import Response

from users.models import TrelloUser
from main.models import Project, Board

from main.serializers.columns import ColumnSerializer
from main.serializers.marks import MarkListSerializer


class BoardListSerializer(serializers.Serializer):
    title = serializers.CharField()
    archived = serializers.BooleanField()
    id = serializers.IntegerField()
    columns = ColumnSerializer(many=True)
    marks = MarkListSerializer(many=True)


class BoardCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    image = serializers.ImageField(default=None)
    project_id = serializers.IntegerField(required=True)

    def create(self, validated_data):
        if not Board.objects.filter(
                Q(title=validated_data.get('title')) & Q(project_id=validated_data.get('project_id'))).exists():
            return Board.objects.create(title=validated_data.get('title'),
                                        archived=False,
                                        image=validated_data.get('image'),
                                        project_id=validated_data.get('project_id'))
        return Response("A board with this name already exists in this project", status=status.HTTP_400_BAD_REQUEST)


class BoardArchiveSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    archived = serializers.CharField(required=True)
    project_id = serializers.IntegerField(required=False)

    def validate(self, attrs):
        if not Board.objects.filter(Q(title=attrs['title']) & Q(project_id=attrs['project_id'])).exists():
            return Response("No board found", status=status.HTTP_404_NOT_FOUND)
        return attrs


class BoardEditSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)

    def validate(self, attrs):
        if Board.objects.filter(title=attrs['title']).exists():
            raise serializers.ValidationError("A board with this name already exists")
        return attrs

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.image = validated_data.get('image')
        instance.save()
        return instance


class BoardAddMembersSerializer(serializers.Serializer):

    members = serializers.ListField()

    def validate(self, attrs):
        for member in attrs['members']:
            if not TrelloUser.objects.filter(username=member).exists():
                raise serializers.ValidationError(f"User {member} not found")
            return attrs


class BoardFavourSerializer(serializers.Serializer):

    id = serializers.IntegerField(required=False)

    def validate(self, attrs):
        if not Board.objects.filter(pk=attrs['id']):
            return Response("Board not found", status=status.HTTP_404_NOT_FOUND)
        return attrs


class BoardFavourListSerializer(serializers.Serializer):

    board_id = serializers.IntegerField(required=False)