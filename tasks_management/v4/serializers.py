from django.core.exceptions import ValidationError
from rest_framework import serializers

from tasks_management.models import Task, ToDoList, Token

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

    def validate_title(self, data):
        if len(data) < 8:
            raise ValidationError("title is too short")
        return data

class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    done = serializers.BooleanField(required=True)
    due_date = serializers.DateField(required=True)
    priority = serializers.ChoiceField(choices=PRIORITY, required=True)
    file = serializers.FileField(required=True)
    list_id = serializers.IntegerField(required=False, write_only=True)

    def create(self, validated_data):
        list_id = validated_data.pop("list_id")
        task = Task.objects.create(**validated_data)
        task.to_do_lists.add(ToDoList.objects.get(id=list_id))
        return task

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.done = validated_data.get("done", instance.done)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.priority = validated_data.get("priority", instance.priority)
        instance.file = validated_data.get("file", instance.file)
        instance.save()
        return instance

    def validate_list_id(self, data):
        if not ToDoList.objects.filter(id=data, user=self.context['request'].user).exists():
            raise ValidationError("invalid id")
        return data


class DeleteTaskSerializer(serializers.Serializer):
    list_id = serializers.IntegerField(required=False, write_only=True)

    def validate_list_id(self, data):
        if not ToDoList.objects.filter(id=data, user=self.context['request'].user).exists():
            raise ValidationError("invalid id")
        return data


class TokenSerializer(serializers.Serializer):
    list_id = serializers.IntegerField(required=True, write_only=True)

    def update(self, instance, validated_data):
        list_id = validated_data["list_id"]
        to_do_list = ToDoList.objects.get(id=list_id)
        instance.to_do_lists.add(to_do_list)
        return instance

    def validate_list_id(self, data):
        if not ToDoList.objects.filter(id=data, user=self.context['request'].user).exists():
            raise ValidationError("invalid id")
        return data


class NewTokenSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    task_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        return Token.objects.create(**validated_data)

    def validate_task_id(self, data):
        if not Task.objects.filter(id=data).exists():
            raise ValidationError("no task with this id")
        if Task.objects.filter(to_do_lists__user=self.context['request'].user).filter(id=data).exists():
            return data
        raise ValidationError("this is another user's task")
