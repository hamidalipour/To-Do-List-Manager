from rest_framework import serializers

from tasks_management.models import ToDoList, Task, Token

PRIORITY = (
    ("High", "High"),
    ("Medium", "Medium"),
    ("Low", "Low"),
)


class ToDoListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()

    def create(self, validated_data):
        return ToDoList.objects.create(**validated_data)


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    done = serializers.BooleanField()
    due_date = serializers.DateField()
    priority = serializers.ChoiceField(choices=PRIORITY)
    file = serializers.FileField()

    def create(self, validated_data):
        return Task.objects.create(**validated_data)


class TokenSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()


class NewTokenSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)

    def create(self, validated_data):
        return Token.objects.create(**validated_data)
