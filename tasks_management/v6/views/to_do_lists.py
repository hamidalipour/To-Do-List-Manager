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
        if self.action in ["create_task_with_uuid"]:
            return TokenSerializer
        return ToDoListSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        for task in instance.task_set.all():
            task.to_do_lists.remove(instance)
            if not task.to_do_lists.exists():
                task.delete()
        return instance.delete()

    @action(detail=True, methods=["POST"])
    def create_task_with_uuid(self, request, pk=None):
        uuid = self.request.query_params['uuid']
        try:
            token = Token.objects.get(uuid=uuid)
            to_do_list = self.get_object()
            token.task.to_do_lists.add(to_do_list)
            return Response("task was added")
        except ValidationError:
            return Response("invalid token format")
        except Token.DoesNotExist:
            return Response("token doesn't exist")
