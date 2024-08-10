from django.conf import settings
from django.shortcuts import redirect
from django.views import View

from personal_to_do_list.models import ToDoList

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


class DeleteToDoListView(View):
    def post(self, request, list_id):
        to_do_list = ToDoList.objects.get(id=list_id)
        for task in to_do_list.task_set.all():
            task.to_do_lists.remove(to_do_list)
            if not task.to_do_lists.exists():
                task.delete()
        to_do_list.delete()
        return redirect(f"{DEFAULT_DOMAIN}v2/to-do-lists")
