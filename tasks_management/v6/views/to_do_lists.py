from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from tasks_management.models import ToDoList, Token
from tasks_management.v6.serializers import ToDoListSerializer, TokenSerializer


class ToDoListsView(viewsets.ModelViewSet):
    def get_queryset(self):
        return ToDoList.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ["add_task_with_uuid"]:
            return TokenSerializer
        return ToDoListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["POST"])
    def add_task_with_uuid(self, request, pk=None):
        to_do_list = self.get_object()
        if to_do_list.user != request.user:
            return Response("to do list doesn't belong to you")
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            uuid = serializer.validated_data['uuid']
            try:
                token = Token.objects.get(uuid=uuid)
            except ValidationError:
                return Response("invalid token format")
            except Token.DoesNotExist:
                return Response("token doesn't exist")
            token.task.to_do_lists.add(to_do_list)
            return Response("task was added")
