from django.db.models import Case, Value, When
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets
from rest_framework.response import Response
from tasks_management.models import Task, ToDoList
from tasks_management.v6.serializers import TaskSerializer, DeleteTaskSerializer


class TasksView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_serializer_class(self):
        if self.action in ["delete"]:
            return DeleteTaskSerializer
        return TaskSerializer

    def get_queryset(self):
        priority_order = Case(
            When(priority=Task.Priority.HIGH, then=Value(1)),
            When(priority=Task.Priority.MEDIUM, then=Value(2)),
            When(priority=Task.Priority.LOW, then=Value(3)),
        )
        tasks = (
            Task.objects.filter(to_do_lists__user=self.request.user)
            .annotate(priority_order=priority_order)
            .order_by("due_date", "priority_order")
        )
        if not self.request.query_params["list_id"].isnumeric() and 'list_id' in self.request.query_params:
            tasks = tasks.filter(to_do_lists__id=self.request.query_params["list_id"])
        return tasks

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DeleteTaskSerializer(instance, data=self.request.data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            to_do_list = ToDoList.objects.get(id=serializer.validated_data['list_id'])
            if instance.to_do_lists.filter(id=to_do_list.id).exists():
                instance.to_do_lists.remove(to_do_list)
            else:
                return Response("task is not in this to do list")
            if not instance.to_do_lists.exists():
                instance.delete()
            return Response("task was deleted")
