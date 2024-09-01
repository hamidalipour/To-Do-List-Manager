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

    #Todo change all validate_list_id like this
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
    list_id = serializers.IntegerField()

    def validate_list_id(self, data):
        if not ToDoList.objects.filter(id=data, user=self.context['request'].user).exists():
            raise ValidationError("invalid id")
        return data


class NewTokenSerializer(serializers.ModelSerializer):
    #Todo get task_id in serializer and validate it and after that delete perform create
    class Meta:
        model = Token
        fields = ["uuid"]
        read_only_fields = ["uuid"]


