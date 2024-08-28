from rest_framework import generics
from rest_framework.response import Response

from tasks_management.models import Task, ToDoList
from tasks_management.v4.serializers import DeleteTaskSerializer


class DeleteTaskView(generics.RetrieveUpdateAPIView):
    serializer_class = DeleteTaskSerializer
    queryset = Task.objects.all()

    def update(self, request, *args, **kwargs):
        if not Task.objects.filter(id=self.kwargs['task_id']).exists():
            return Response("invalid id")
        instance = Task.objects.get(id=self.kwargs['task_id'])
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        to_do_list = ToDoList.objects.get(id=serializer.validated_data['list_id'])
        if to_do_list.user != self.request.user:
            return Response("it is not your to do list")
        if instance.to_do_lists.filter(id=to_do_list.id).exists():
            instance.to_do_lists.remove(to_do_list)
        else:
            return Response("task is not in this to do list")
        if not instance.to_do_lists.exists():
            instance.delete()
        return Response(serializer.data)


