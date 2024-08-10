from django.shortcuts import redirect
from django.views import View

from personal_to_do_list.models import Task, ToDoList
from django.conf import settings

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


class DeleteTaskView(View):
    def post(self, request, task_id, list_id):
        task = Task.objects.get(id=task_id)
        to_do_list = ToDoList.objects.get(id=list_id)
        task.to_do_lists.remove(to_do_list)
        if not task.to_do_lists.exists():
            task.delete()
        return redirect(f"{DEFAULT_DOMAIN}v2/to-do-lists/{list_id}")
