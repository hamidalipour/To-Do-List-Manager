from django.core.exceptions import ValidationError
from rest_framework import generics
from rest_framework.response import Response

from tasks_management.models import Task, ToDoList, Token
from tasks_management.v4.serializers import TokenSerializer


class CreateTaskWithUuidView(generics.RetrieveUpdateAPIView):
    serializer_class = TokenSerializer
    queryset = Task.objects.all()
    lookup_field = "uuid"

    def get_object(self):
        token = Token.objects.get(uuid=self.kwargs['uuid'])
        return token.task
