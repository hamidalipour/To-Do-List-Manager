from django.conf import settings
from django.shortcuts import redirect, render

from personal_to_do_list.models import Task, ToDoList, Token

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


def handle_task(request, task_id, list_id):
    token = None
    task = Task.objects.get(id=task_id)
    to_do_list = ToDoList.objects.get(id=list_id)
    if request.method == 'POST' and "create_token" in request.POST:
        token = Token.objects.create(task=task)
        token = token.uuid
    elif request.method == 'POST' and "delete_task" in request.POST:
        task.to_do_lists.remove(to_do_list)
        if not task.to_do_lists.exists():
            task.delete()
        return redirect(f"{DEFAULT_DOMAIN}v1/to-do-lists/{list_id}")

    return render(request, 'handle-task.html',
                  context={'task': task, 'token': token, 'version': "v1", 'default_domain': DEFAULT_DOMAIN,
                           'list_id': list_id})
