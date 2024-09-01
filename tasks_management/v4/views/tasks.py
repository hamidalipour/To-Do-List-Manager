from django.db.models import Case, Value, When
from rest_framework import generics
from rest_framework.response import Response
from tasks_management.models import Task, ToDoList
from tasks_management.v4.serializers import TaskSerializer


class TasksView(generics.ListAPIView):
    serializer_class = TaskSerializer

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
        if not self.request.query_params["list_id"].isnumeric():
            return tasks
        if 'list_id' in self.request.query_params:
            tasks = tasks.filter(to_do_lists__id=self.request.query_params["list_id"])
        return tasks
