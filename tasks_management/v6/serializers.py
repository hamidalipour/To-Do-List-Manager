from django.core.exceptions import ValidationError
from rest_framework import serializers

from tasks_management.models import Task, ToDoList, Token

PRIORITY = (
    ("High", "High"),
    ("Medium", "Medium"),
    ("Low", "Low"),
)


class ToDoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = ["id", "title"]
        read_only_fields = ["id"]

    def validate_title(self, data):
        if len(data) < 8:
            raise ValidationError("title is too short")
        return data


class TaskSerializer(serializers.ModelSerializer):
    list_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Task
        fields = ["id", "title", "description", "done", "due_date", "priority", "file", "list_id"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        list_id = validated_data.pop("list_id")
        task = Task.objects.create(**validated_data)
        task.to_do_lists.add(ToDoList.objects.get(id=list_id))
        return task

    def update(self, instance, validated_data):
        if 'list_id' in validated_data:
            validated_data.pop('list_id')
        return super().update(instance, validated_data)

    def validate_list_id(self, data):
        if not ToDoList.objects.filter(id=data, user=self.context['request'].user).exists():
            raise ValidationError("invalid id")
        return data


class DeleteTaskSerializer(serializers.Serializer):
    list_id = serializers.IntegerField(write_only=True)

    def validate_list_id(self, data):
        if not ToDoList.objects.filter(id=data, user=self.context['request'].user).exists():
            raise ValidationError("invalid id")
        return data


class TokenSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()


class NewTokenSerializer(serializers.ModelSerializer):
    task_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Token
        fields = ["uuid", "task_id"]
        read_only_fields = ["uuid"]

    def validate_task_id(self, data):
        if not Task.objects.filter(to_do_lists__user=self.context['request'].user).filter(id=data).exists():
            raise ValidationError("invalid id")
        return data
