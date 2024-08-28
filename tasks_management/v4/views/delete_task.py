from rest_framework import generics
from rest_framework.response import Response

from tasks_management.models import Task, ToDoList
from tasks_management.v4.serializers import TaskSerializer


class DeleteTaskView(generics.RetrieveUpdateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_object(self):
        return Task.objects.get(id=self.kwargs['task_id'])

    #ToDo override update instead
    def perform_update(self, serializer):
        try:
            instance = self.get_object()
            to_do_list = ToDoList.objects.get(id=serializer.validated_data['list_id'])
            if to_do_list.user != self.request.user:
                return Response("it is not your to do list")
            if instance.to_do_lists.filter(id=to_do_list.id).exists():
                instance.to_do_lists.remove(to_do_list)
            else:
                return Response("task is not in this to do list")
            if not instance.to_do_lists.exists():
                instance.delete()
            return Response("task was deleted")
        except Task.DoesNotExist:
            return Response("Invalid id")
