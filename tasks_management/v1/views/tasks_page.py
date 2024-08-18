from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Case, Value, When
from django.shortcuts import render
from django.urls import reverse

from tasks_management import forms
from tasks_management.models import Task, ToDoList, Token

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


def tasks_page(request, list_id):
    priority_order = Case(
        When(priority=Task.Priority.HIGH, then=Value(1)),
        When(priority=Task.Priority.MEDIUM, then=Value(2)),
        When(priority=Task.Priority.LOW, then=Value(3)),
    )
    tasks = (
        Task.objects.filter(to_do_lists__id=list_id)
        .annotate(priority_order=priority_order)
        .order_by("due_date", "priority_order")
    )
    form = forms.TokenForm()
    message = ""
    if request.method == "POST":
        form = forms.TokenForm(request.POST)
        if form.is_valid():
            uuid = form.cleaned_data["uuid"]
            try:
                token = Token.objects.get(uuid=uuid)
                to_do_list = ToDoList.objects.get(id=list_id)
                token.task.to_do_lists.add(to_do_list)
                message = "task has been added"
            except ValidationError:
                message = "invalid token format"
            except Token.DoesNotExist:
                message = "token doesn't exist"
    default_url = f"{DEFAULT_DOMAIN}v1"
    create_task_url = reverse("create-task-v1", kwargs={"list_id": list_id})
    create_with_uuid_url = reverse(
        "create-task-with-uuid-v1", kwargs={"list_id": list_id}
    )
    delete_to_do_list_url = reverse("delete-to-do-list-v1", kwargs={"list_id": list_id})
    return render(
        request,
        "tasks.html",
        context={
            "tasks": tasks,
            "list_id": list_id,
            "form": form,
            "message": message,
            "default_url": default_url,
            "create_task_url": create_task_url,
            "create_with_uuid_url": create_with_uuid_url,
            "delete_to_do_list_url": delete_to_do_list_url,
        },
    )
