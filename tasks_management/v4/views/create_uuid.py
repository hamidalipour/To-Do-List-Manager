from rest_framework import generics
from rest_framework.response import Response
from tasks_management.models import Task, Token
from tasks_management.v4.serializers import NewTokenSerializer


class CreateUuidView(generics.CreateAPIView):
    serializer_class = NewTokenSerializer
    queryset = Token.objects.all()

    def perform_create(self, serializer):
        task = Task.objects.get(id=serializer.validated_data["task_id"])
        serializer.save(task=task)