from django.db.models import Case, Value, When
from rest_framework import viewsets
from rest_framework.response import Response

from tasks_management.models import Task, ToDoList
from tasks_management.v5.serializers import TaskSerializer


class TasksView(viewsets.ViewSet):
    def list(self, request, list_id):
        priority_order = Case(
            When(priority=Task.Priority.HIGH, then=Value(1)),
            When(priority=Task.Priority.MEDIUM, then=Value(2)),
            When(priority=Task.Priority.LOW, then=Value(3)),
        )
        queryset = (
            Task.objects.filter(to_do_lists__id=list_id)
            .annotate(priority_order=priority_order)
            .order_by("due_date", "priority_order")
        )
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, list_id):
        queryset = Task.objects.all()
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            task = serializer.save()
            task.to_do_lists.add(ToDoList.objects.get(id=list_id))
            return Response(serializer.data)

    def destroy(self, request, task_id, list_id):
        try:
            task = Task.objects.get(id=task_id)
            to_do_list = ToDoList.objects.get(id=list_id)
            if task.to_do_lists.filter(id=to_do_list.id).exists():
                task.to_do_lists.remove(to_do_list)
            else:
                return Response("task is not in this to do list")
            if not task.to_do_lists.exists():
                task.delete()
            return Response("task was deleted")
        except Task.DoesNotExist:
            return Response("Invalid id")

    def update(self, request, task_id):
        queryset = Task.objects.all()
        task = Task.objects.get(id=task_id)
        serializer = TaskSerializer(instance=task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.error_messages)
