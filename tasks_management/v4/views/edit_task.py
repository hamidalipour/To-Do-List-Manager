from rest_framework import generics
from rest_framework.response import Response

from tasks_management.models import Task
from tasks_management.v4.serializers import TaskSerializer


class EditTaskView(generics.RetrieveUpdateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_field = "id"

    def get_object(self):
        return Task.objects.get(id=self.kwargs["task_id"])

    #ToDo override update instead
    def perform_update(self, serializer):
        instance = self.get_object()
        for to_do_list in instance.to_do_lists.all():
            if to_do_list.user == self.request.user:
                return serializer.save(instance=instance)
        return Response("this task doesn't belong to you")

    #Todo check if it is needed
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = TaskSerializer(instance)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response("id is not valid")
