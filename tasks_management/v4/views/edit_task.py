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

    def update(self, request, *args, **kwargs):
        if not Task.objects.filter(id=self.kwargs['task_id']).exists():
            return Response("invalid task id")
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        if Task.objects.filter(to_do_lists__user=self.request.user).filter(id=instance.id).exists():
            serializer.save(instance=instance)
            return Response(serializer.data)
        return Response("this task doesn't belong to you")
