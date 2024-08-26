from rest_framework import generics

from tasks_management.models import Task, ToDoList
from tasks_management.v4.serializers import TaskSerializer


class CreateTask(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        task = serializer.save()
        task.to_do_lists.add(ToDoList.objects.get(id=serializer.validated_data['list_id']))
        return task

    # def get_serializer_context(self):
    #     return {
    #         'request': self.request,
    #         'format': self.format_kwarg,
    #         'view': self
    #     }
