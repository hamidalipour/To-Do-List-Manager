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

    def perform_update(self, serializer):
        instance = self.get_object()
        return serializer.save(instance=instance)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = TaskSerializer(instance)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response("id is not valid")
