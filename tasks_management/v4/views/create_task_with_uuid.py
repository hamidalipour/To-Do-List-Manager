from django.core.exceptions import ValidationError
from rest_framework import generics

from tasks_management.models import Task, Token, ToDoList
from tasks_management.v4.serializers import TokenSerializer
from rest_framework.response import Response


class CreateTaskWithUuidView(generics.CreateAPIView):
    serializer_class = TokenSerializer
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        uuid = serializer.validated_data['uuid']
        try:
            token = Token.objects.get(uuid=uuid)
            to_do_list = ToDoList.objects.get(id=self.kwargs['list_id'])
            token.task.to_do_lists.add(to_do_list)
            return token.task
        except ValidationError:
            return Response("invalid token format")
        except Token.DoesNotExist:
            return Response("token doesn't exist")

