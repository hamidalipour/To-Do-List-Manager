from rest_framework import serializers

from tasks_management.models import ToDoList, Task, Token

PRIORITY = (
    ("High", "High"),
    ("Medium", "Medium"),
    ("Low", "Low"),
)


class ToDoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = ['id', 'title']
        read_only_fields = ['id']

    def create(self, validated_data):
        return ToDoList.objects.create(**validated_data)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "done", "due_date", "priority", "file"]
        read_only_fields = ['id']

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.done = validated_data.get('done', instance.done)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.file = validated_data.get('file', instance.file)
        instance.save()
        return instance


class TokenSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()


class NewTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ["uuid"]
        read_only_fields = ["uuid"]

    def create(self, validated_data):
        return Token.objects.create(**validated_data)
