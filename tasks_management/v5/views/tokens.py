from rest_framework import viewsets
from rest_framework.response import Response

from tasks_management.models import Task, Token
from tasks_management.v5.serializers import NewTokenSerializer


class TokenView(viewsets.ViewSet):
    def create(self, request, task_id):
        serializer = NewTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            task = Task.objects.get(id=task_id)
            for to_do_list in task.to_do_lists.all():
                if to_do_list.user == self.request.user:
                    serializer.save(task=task)
                    return Response(serializer.data)
            return Response("task doesn't belong to you")
