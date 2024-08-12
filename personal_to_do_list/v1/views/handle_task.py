from django.conf import settings
from django.shortcuts import render

from personal_to_do_list.models import Task, Token

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


def handle_task(request, task_id, list_id):
    token = None
    task = Task.objects.get(id=task_id)
    if request.method == "POST" and "create_token" in request.POST:
        token = Token.objects.create(task=task)
        token = token.uuid
    return render(
        request,
        "handle-task.html",
        context={
            "task": task,
            "token": token,
            "version": "v1",
            "default_domain": DEFAULT_DOMAIN,
            "list_id": list_id,
        },
    )
