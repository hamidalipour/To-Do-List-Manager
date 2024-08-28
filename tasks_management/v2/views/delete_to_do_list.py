from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from tasks_management.models import ToDoList


class DeleteToDoListView(View):
    def post(self, request, list_id):
        to_do_list = ToDoList.objects.get(id=list_id)
        to_do_list.delete()
        return redirect(reverse("to-do-lists-page-v2"))
