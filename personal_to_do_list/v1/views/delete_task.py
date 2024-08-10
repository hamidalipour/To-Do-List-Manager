from django.conf import settings
from django.shortcuts import redirect

from personal_to_do_list.models import Task, ToDoList

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


def delete_task(request, task_id, list_id):
    task = Task.objects.get(id=task_id)
    to_do_list = ToDoList.objects.get(id=list_id)
    task.to_do_lists.remove(to_do_list)
    if not task.to_do_lists.exists():
        task.delete()
    return redirect(f"{DEFAULT_DOMAIN}v1/to-do-lists/{list_id}")
