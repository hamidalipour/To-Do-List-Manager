from django.db.models import Case, Value, When
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics

from tasks_management.models import Task, ToDoList
from tasks_management.v4.serializers import TaskSerializer


class TasksView(generics.ListAPIView):
    serializer_class = TaskSerializer

    #Todo check with if not try catch
    def get_queryset(self):
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
                return None
        except MultiValueDictKeyError:
            tasks = (
                Task.objects.filter(to_do_lists__user=self.request.user)
                .annotate(priority_order=priority_order)
                .order_by("due_date", "priority_order")
            )
        except ToDoList.DoesNotExist:
            return None

        return tasks
