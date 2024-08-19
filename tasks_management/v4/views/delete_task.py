from rest_framework import generics
from rest_framework.response import Response

from tasks_management.models import Task, ToDoList
from tasks_management.v4.serializer import TaskSerializer


class DeleteTaskView(generics.DestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            task = Task.objects.get(id=self.kwargs['task_id'])
            to_do_list = ToDoList.objects.get(id=self.kwargs['list_id'])
            if task.to_do_lists.filter(id=to_do_list.id).exists():
                task.to_do_lists.remove(to_do_list)
            else:
                return Response("task is not in this to do list")
            if not task.to_do_lists.exists():
                task.delete()
            return Response("task was deleted")
        except Task.DoesNotExist:
            return Response("Invalid id")
