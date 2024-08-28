from rest_framework import generics
from rest_framework.response import Response
from tasks_management.models import Task, Token
from tasks_management.v4.serializers import NewTokenSerializer


class CreateUuidView(generics.CreateAPIView):
    serializer_class = NewTokenSerializer
    queryset = Token.objects.all()

    def perform_create(self, serializer):
        task = Task.objects.get(id=self.kwargs["task_id"])
        #Task.objects.filter(to_do_lists__user=self.request.user).exists()
        #ToDo validate task id in serializer
        for to_do_list in task.to_do_lists.all():
            if to_do_list.user == self.request.user:
                return serializer.save(task=task)