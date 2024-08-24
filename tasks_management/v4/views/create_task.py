from rest_framework import generics

from tasks_management.models import Task, ToDoList
from tasks_management.v4.serializers import TaskSerializer


class CreateTask(generics.CreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        task = serializer.save()
        task.to_do_lists.add(ToDoList.objects.get(id=self.kwargs["list_id"]))
        return task
