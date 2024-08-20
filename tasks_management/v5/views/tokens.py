from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.response import Response

from tasks_management.models import ToDoList, Task, Token
from tasks_management.v5.serializers import NewTokenSerializer, TokenSerializer


class TokenView(viewsets.ViewSet):
    def create(self, request, task_id):
        queryset = Token.objects.all()
        serializer = NewTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            task = Task.objects.get(id=task_id)
            serializer.save(task=task)
            return Response(serializer.data)
