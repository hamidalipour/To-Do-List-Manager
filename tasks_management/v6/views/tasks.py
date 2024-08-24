from django.db.models import Case, Value, When
from rest_framework import viewsets

from tasks_management.models import Task, ToDoList
from tasks_management.v6.serializers import TaskSerializer


class TasksView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        priority_order = Case(
            When(priority=Task.Priority.HIGH, then=Value(1)),
            When(priority=Task.Priority.MEDIUM, then=Value(2)),
            When(priority=Task.Priority.LOW, then=Value(3)),
        )
        tasks = (
            Task.objects.filter(to_do_lists__id=self.request.POST["list_id"])
            .annotate(priority_order=priority_order)
            .order_by("due_date", "priority_order")
        )
        return tasks

    def perform_create(self, serializer):
        task = serializer.save()
        task.to_do_lists.add(ToDoList.objects.get(id=self.request.POST["list_id"]))
        return task

    def perform_destroy(self, instance):
        to_do_list = ToDoList.objects.get(id=self.request.POST["list_id"])
        if instance.to_do_lists.filter(id=to_do_list.id).exists():
            instance.to_do_lists.remove(to_do_list)
        if not instance.to_do_lists.exists():
            instance.delete()
