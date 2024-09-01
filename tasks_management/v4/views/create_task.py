from rest_framework import generics

from tasks_management.models import Task, ToDoList
from tasks_management.v4.serializers import TaskSerializer


class CreateTask(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
