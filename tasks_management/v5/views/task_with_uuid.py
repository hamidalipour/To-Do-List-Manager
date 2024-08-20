from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.response import Response

from tasks_management.models import ToDoList, Task, Token
from tasks_management.v5.serializers import NewTokenSerializer, TokenSerializer


class TaskWithUuid(viewsets.ViewSet):

    def create(self, request, list_id):
        serializer = TokenSerializer(data=request.data)
        queryset = Task.objects.all()
        if serializer.is_valid(raise_exception=True):
            uuid = serializer.validated_data['uuid']
            try:
                token = Token.objects.get(uuid=uuid)
                to_do_list = ToDoList.objects.get(id=self.kwargs['list_id'])
                token.task.to_do_lists.add(to_do_list)
                return Response("task was added")
            except ValidationError:
                return Response("invalid token format")
            except Token.DoesNotExist:
                return Response("token doesn't exist")
        return Response(serializer.error_messages)

