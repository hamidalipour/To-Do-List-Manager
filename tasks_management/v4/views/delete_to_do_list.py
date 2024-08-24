from rest_framework import generics
from rest_framework.response import Response

from tasks_management.models import ToDoList
from tasks_management.v4.serializers import ToDoListSerializer


class DeleteToDoListView(generics.DestroyAPIView):
    serializer_class = ToDoListSerializer
    queryset = ToDoList.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            to_do_list = self.queryset.get(id=self.kwargs["list_id"])
            for task in to_do_list.task_set.all():
                task.to_do_lists.remove(to_do_list)
                if not task.to_do_lists.exists():
                    task.delete()
            to_do_list.delete()
            return Response("to do list was deleted")
        except ToDoList.DoesNotExist:
            return Response("Invalid id")
