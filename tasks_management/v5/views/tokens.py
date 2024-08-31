from rest_framework import viewsets
from rest_framework.response import Response

from tasks_management.models import Task, Token
from tasks_management.v5.serializers import NewTokenSerializer


class TokenView(viewsets.ViewSet):
    def create(self, request, task_id):
        serializer = NewTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if Task.objects.filter(to_do_lists__user=self.request.user).filter(id=task_id).exists():
                task = Task.objects.get(id=task_id)
                serializer.save(task=task)
                return Response(serializer.data)

            return Response("task doesn't belong to you")
