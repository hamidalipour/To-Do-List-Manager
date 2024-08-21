from rest_framework import viewsets
from rest_framework.response import Response
from tasks_management.models import ToDoList
from tasks_management.v6.serializers import ToDoListSerializer


class ToDoListsView(viewsets.ModelViewSet):
    queryset = ToDoList.objects.all()
    serializer_class = ToDoListSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        for task in instance.task_set.all():
            task.to_do_lists.remove(instance)
            if not task.to_do_lists.exists():
                task.delete()
        return instance.delete()
