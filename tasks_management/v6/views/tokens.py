from rest_framework import viewsets

from tasks_management.models import Task, Token
from tasks_management.v6.serializers import NewTokenSerializer


class TokensView(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = NewTokenSerializer

    def perform_create(self, serializer):
        task = Task.objects.get(id=self.request.POST["task_id"])
        return serializer.save(task=task)
