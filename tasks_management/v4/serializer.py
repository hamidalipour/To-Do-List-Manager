from rest_framework import serializers

from tasks_management.models import ToDoList, Task

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

