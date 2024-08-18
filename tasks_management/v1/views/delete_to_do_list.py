from django.shortcuts import redirect
from django.urls import reverse

from tasks_management.models import ToDoList


def delete_to_do_list(request, list_id):
    to_do_list = ToDoList.objects.get(id=list_id)
    for task in to_do_list.task_set.all():
        task.to_do_lists.remove(to_do_list)
        if not task.to_do_lists.exists():
            task.delete()
    to_do_list.delete()
    return redirect(reverse("to-do-lists-page-v1"))
