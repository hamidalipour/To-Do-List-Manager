from django.shortcuts import render
from django.urls import reverse
from django.views import View

from tasks_management.models import Task, Token


class HandleTaskView(View):
    def get(self, request, task_id, list_id):
        token = None
        task = Task.objects.get(id=task_id)
        create_url = reverse(
            "create-uuid-v2", kwargs={"list_id": list_id, "task_id": task_id}
        )
        delete_url = reverse(
            "delete-task-v2", kwargs={"list_id": list_id, "task_id": task_id}
        )
        edit_url = reverse(
            "edit-task-v2", kwargs={"list_id": list_id, "task_id": task_id}
        )
        return render(
            request,
            "handle-task.html",
            context={
                "task": task,
                "token": token,
                "create_url": create_url,
                "delete_url": delete_url,
                "list_id": list_id,
                "edit_url": edit_url,
            },
        )

    def post(self, request, task_id, list_id):
        task = Task.objects.get(id=task_id)
        create_url = reverse(
            "create-uuid-v2", kwargs={"list_id": list_id, "task_id": task_id}
        )
        delete_url = reverse(
            "delete-task-v2", kwargs={"list_id": list_id, "task_id": task_id}
        )
        edit_url = reverse(
            "edit-task-v2", kwargs={"list_id": list_id, "task_id": task_id}
        )
        if "create_token" in request.POST:
            token = Token.objects.create(task=task)
            token = token.uuid
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
