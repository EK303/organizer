from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed

from django.shortcuts import get_object_or_404
from main.models import Project
from users.models import TrelloUser


class ProjectListSerializer(serializers.Serializer):
    title = serializers.CharField()
    creator = serializers.CharField()
    id = serializers.IntegerField()


class ProjectCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=30, required=True)
    creator_username = serializers.CharField(required=False)

    def validate(self, attrs):
        if Project.objects.filter(title=attrs['title']).exists():
            raise MethodNotAllowed("A project with this name already exists")
        return attrs

    def create(self, validated_data):
        user = TrelloUser.objects.get(username=validated_data.get("creator_username"))
        return Project.objects.create(title=validated_data.get("title"),
                                      creator=user)


class BoardsSerializer(serializers.Serializer):
    title = serializers.CharField()
    id = serializers.IntegerField()


class ProjectViewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    boards = BoardsSerializer(many=True)


class ProjectEditSerializer(serializers.Serializer):
    title = serializers.CharField()

    def validate(self, attrs):
        if Project.objects.filter(title=attrs['title']).exists():
            raise MethodNotAllowed("A project with this name already exists")
        return attrs

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title")
        instance.save()
        return instance


