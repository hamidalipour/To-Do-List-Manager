from rest_framework import generics

from tasks_management.models import Token, Task
from tasks_management.v4.serializers import NewTokenSerializer


class CreateUuidView(generics.CreateAPIView):
    serializer_class = NewTokenSerializer
    queryset = Token.objects.all()

    def perform_create(self, serializer):
        task = Task.objects.get(id=self.kwargs['task_id'])
        return serializer.save(task=task)
