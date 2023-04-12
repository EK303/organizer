from rest_framework import serializers

from main.models import Card

from users.serializers import UserSerializer


class CommentCreateSerializer(serializers.Serializer):
    body = serializers.CharField()


class CommentListSerializer(serializers.Serializer):
    body = serializers.CharField()
    author = UserSerializer()
    created_on = serializers.DateTimeField()


class CardListSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    due_date = serializers.DateField()
    checklist = serializers.JSONField()
    comments = CommentListSerializer(many=True)


class CardCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    due_date = serializers.DateField(required=False, allow_null=True, default="")
    column_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return Card.objects.create(title=validated_data.get("title"),
                                   description=validated_data.get("description"),
                                   due_date=validated_data.get("due_date"),
                                   checklist=validated_data.get("checklist"),
                                   column_id=validated_data.get("column_id"))


class CardEditSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    due_date = serializers.DateField(required=False, allow_null=True, default=None)
    checklist = serializers.JSONField(required=False, read_only=True)
    column_id = serializers.IntegerField(required=False)

    def validate(self, attrs):
        return attrs

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.checklist = validated_data.get("checklist")
        instance.column_id = validated_data.get("column_id", instance.column_id)
        instance.save()
        return instance
