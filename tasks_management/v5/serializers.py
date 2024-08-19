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


class NewTokenSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)

    def create(self, validated_data):
        return Token.objects.create(**validated_data)
