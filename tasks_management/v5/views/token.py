from rest_framework import viewsets
from rest_framework.response import Response

from tasks_management.models import ToDoList, Task
from tasks_management.v5.serializers import TaskSerializer, ToDoListSerializer
from django.db.models import Case, When, Value

class TokenView(viewsets.ViewSet):
    def create(self, request, task_id):
        pass