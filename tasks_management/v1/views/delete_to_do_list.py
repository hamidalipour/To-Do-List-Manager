from django.shortcuts import redirect
from django.urls import reverse

from tasks_management.models import ToDoList


def delete_to_do_list(request, list_id):
    to_do_list = ToDoList.objects.get(id=list_id)
    to_do_list.delete()
    return redirect(reverse("to-do-lists-page-v1"))
