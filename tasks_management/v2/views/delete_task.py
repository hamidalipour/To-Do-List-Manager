from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from tasks_management.models import Task, ToDoList


class DeleteTaskView(View):
    def post(self, request, task_id, list_id):
        task = Task.objects.get(id=task_id)
        to_do_list = ToDoList.objects.get(id=list_id)
        task.to_do_lists.remove(to_do_list)
        if not task.to_do_lists.exists():
            task.delete()
        return redirect(reverse("tasks-page-v2", kwargs={"list_id": list_id}))
