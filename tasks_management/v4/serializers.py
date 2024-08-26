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


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    done = serializers.BooleanField(required=True)
    due_date = serializers.DateField(required=True)
    priority = serializers.ChoiceField(choices=PRIORITY, required=True)
    file = serializers.FileField(required=True)
    list_id = serializers.IntegerField(required=True, write_only=True)

    def create(self, validated_data):
        validated_data_copy = validated_data.copy()
        validated_data_copy.pop("list_id")
        print(validated_data_copy)
        print(validated_data)
        return Task.objects.create(**validated_data_copy)
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
        try:
            to_do_list = ToDoList.objects.get(id=data)
            if to_do_list.user == self.context['request'].user:
                return data
            return ValidationError("this is another user's to do list")
        except ToDoList.DoesNotExist:
            return ValidationError("no to do list with this id")



class TokenSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()


class NewTokenSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)

    def create(self, validated_data):
        return Token.objects.create(**validated_data)
