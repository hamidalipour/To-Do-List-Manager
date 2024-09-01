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

    def create(self, validated_data):
        return ToDoList.objects.create(**validated_data)


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

    def validate_list_id(self, data):
        if not ToDoList.objects.filter(id=data, user=self.context['request'].user).exists():
            raise ValidationError("invalid id")
        return data


class UpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "done", "due_date", "priority", "file"]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.done = validated_data.get("done", instance.done)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.priority = validated_data.get("priority", instance.priority)
        instance.file = validated_data.get("file", instance.file)
        instance.save()
        return instance


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
    class Meta:
        model = Token
        fields = ["uuid"]
        read_only_fields = ["uuid"]

    def create(self, validated_data):
        return Token.objects.create(**validated_data)
