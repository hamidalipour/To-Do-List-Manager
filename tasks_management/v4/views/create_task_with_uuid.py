from django.core.exceptions import ValidationError
from rest_framework import generics
from rest_framework.response import Response

from tasks_management.models import Task, ToDoList, Token
from tasks_management.v4.serializers import TokenSerializer


class CreateTaskWithUuidView(generics.RetrieveUpdateAPIView):
    serializer_class = TokenSerializer
    queryset = Task.objects.all()
    lookup_field = "uuid"

    #Todo uuid should go to url not be a query param
    def get_object(self):
        token = Token.objects.get(uuid=self.request.query_params['uuid'])
        return token.task

#Todo should go to serializer
    def perform_update(self, serializer):
        list_id = serializer.validated_data["list_id"]
        instance = self.get_object()
        to_do_list = ToDoList.objects.get(id=list_id)
        instance.to_do_lists.add(to_do_list)
