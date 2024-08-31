from rest_framework import viewsets

from tasks_management.models import Task, Token
from tasks_management.v6.serializers import NewTokenSerializer
from rest_framework.response import Response


class TokensView(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = NewTokenSerializer

    def perform_create(self, serializer):
        if serializer.is_valid(raise_exception=True):
            task = Task.objects.get(id=self.request.POST["task_id"])
            if Task.objects.filter(to_do_lists__user=self.request.user).filter(id=task.id).exists():
                serializer.save(task=task)
                return Response(serializer.data)
            return Response("task doesn't belong to you")

