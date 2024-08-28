from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.response import Response

from tasks_management.models import Task, ToDoList, Token
from tasks_management.v5.serializers import TokenSerializer


class TaskWithUuid(viewsets.ViewSet):
    def create(self, request):
        serializer = TokenSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            uuid = self.request.query_params['uuid']
            #Todo move lines out of try catch
            try:
                token = Token.objects.get(uuid=uuid)
                to_do_list = serializer.validated_data["list_id"]
                token.task.to_do_lists.add(to_do_list)
                return Response("task was added")
            except ValidationError:
                return Response("invalid token format")
            except Token.DoesNotExist:
                return Response("token doesn't exist")
        return Response(serializer.error_messages)
