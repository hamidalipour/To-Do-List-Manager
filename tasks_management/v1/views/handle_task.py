from django.shortcuts import render
from django.urls import reverse

from tasks_management.models import Task, Token


def handle_task(request, task_id, list_id):
    token = None
    task = Task.objects.get(id=task_id)
    if request.method == "POST" and "create_token" in request.POST:
        token = Token.objects.create(task=task)
        token = token.uuid
    create_url = reverse(
        "create-uuid-v1", kwargs={"list_id": list_id, "task_id": task_id}
    )
    delete_url = reverse(
        "delete-task-v1", kwargs={"list_id": list_id, "task_id": task_id}
    )
    edit_url = reverse("edit-task-v1", kwargs={"list_id": list_id, "task_id": task_id})
    return render(
        request,
        "handle-task.html",
        context={
            "task": task,
            "token": token,
            "create_url": create_url,
            "delete_url": delete_url,
            "edit_url": edit_url,
        },
    )
