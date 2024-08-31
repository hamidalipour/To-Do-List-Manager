from django.db.models import Case, Value, When
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from tasks_management.models import Task, ToDoList
from tasks_management.v5.serializers import TaskSerializer, DeleteTaskSerializer, UpdateTaskSerializer


class TasksView(viewsets.ViewSet):
    def list(self, request):
        priority_order = Case(
            When(priority=Task.Priority.HIGH, then=Value(1)),
            When(priority=Task.Priority.MEDIUM, then=Value(2)),
            When(priority=Task.Priority.LOW, then=Value(3)),
        )

        try:
            to_do_list = ToDoList.objects.get(id=self.request.query_params['list_id'])
            if to_do_list.user == self.request.user:
                tasks = (
                    Task.objects.filter(to_do_lists__id=self.request.query_params["list_id"])
                    .annotate(priority_order=priority_order)
                    .order_by("due_date", "priority_order")
                )
            else:
                return Response("this to do list doesn't belong to you")
        except MultiValueDictKeyError:
            tasks = (
                Task.objects.filter(to_do_lists__user=self.request.user)
                .annotate(priority_order=priority_order)
                .order_by("due_date", "priority_order")
            )
        except ToDoList.DoesNotExist:
            return Response("invalid to do list id")

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            task = serializer.save()
            return Response(serializer.data)

    @action(detail=True, methods=["PATCH"])
    def delete_task(self, request, task_id):
        task = Task.objects.get(id=task_id)
        serializer = DeleteTaskSerializer(task, data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            to_do_list = ToDoList.objects.get(id=serializer.validated_data['list_id'])
            if task.to_do_lists.filter(id=to_do_list.id).exists():
                task.to_do_lists.remove(to_do_list)
            else:
                return Response("task is not in this to do list")
            if not task.to_do_lists.exists():
                task.delete()
            return Response("task was deleted")

    def update(self, request, task_id):
        if Task.objects.filter(to_do_lists__user=self.request.user).filter(id=task_id).exists():
            task = Task.objects.get(id=task_id)
            serializer = UpdateTaskSerializer(instance=task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.error_messages)
        return Response("task doesn't belong to you")
