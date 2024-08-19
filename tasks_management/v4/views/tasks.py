from django.db.models import Case, When, Value
from rest_framework import generics

from tasks_management.models import Task
from tasks_management.v4.serializer import TaskSerializer


class TasksView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        priority_order = Case(
            When(priority=Task.Priority.HIGH, then=Value(1)),
            When(priority=Task.Priority.MEDIUM, then=Value(2)),
            When(priority=Task.Priority.LOW, then=Value(3)),
        )
        tasks = (
            Task.objects.filter(to_do_lists__id=self.kwargs['list_id'])
            .annotate(priority_order=priority_order)
            .order_by("due_date", "priority_order")
        )
        return tasks
