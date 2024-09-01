from rest_framework import generics
from rest_framework.response import Response

from tasks_management.models import Task
from tasks_management.v4.serializers import TaskSerializer


class EditTaskView(generics.RetrieveUpdateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(to_do_lists__user=self.request.user).distinct()

