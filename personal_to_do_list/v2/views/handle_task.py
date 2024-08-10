from django.shortcuts import render, redirect
from django.views import View

from personal_to_do_list.models import Task, Token, ToDoList
from django.conf import settings

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


class HandleTaskView(View):
    def get(self, request, task_id, list_id):
        token = None
        task = Task.objects.get(id=task_id)
        return render(request, 'handle-task.html',
                      context={'task': task, 'token': token, 'version': "v2", 'default_domain': DEFAULT_DOMAIN,
                               'list_id': list_id})

    def post(self, request, task_id, list_id):
        task = Task.objects.get(id=task_id)
        to_do_list = ToDoList.objects.get(id=list_id)
        if "create_token" in request.POST:
            token = Token.objects.create(task=task)
            token = token.uuid
            return render(request, 'handle-task.html',
                          context={'task': task, 'token': token, 'version': "v2", 'default_domain': DEFAULT_DOMAIN,
                                   'list_id': list_id})
        elif "delete_task" in request.POST:
            task.to_do_lists.remove(to_do_list)
            if not task.to_do_lists.exists():
                task.delete()
            return redirect(f"{DEFAULT_DOMAIN}v2/to-do-lists/{list_id}")
