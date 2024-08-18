from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse

from tasks_management.models import Task
from tasks_management.v1 import non_model_forms


def edit_task(request, list_id, task_id):
    task = Task.objects.get(id=task_id)
    form = non_model_forms.TaskForm(
        initial={
            "title": task.title,
            "description": task.description,
            "done": task.done,
            "due_date": task.due_date,
            "priority": task.priority,
            "file": task.file,
        }
    )

    if request.method == "POST":
        form = non_model_forms.TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task.title = form.cleaned_data["title"]
            task.description = form.cleaned_data["description"]
            task.done = form.cleaned_data["done"]
            task.due_date = form.cleaned_data["due_date"]
            task.priority = form.cleaned_data["priority"]
            if "file" in request.FILES:
                task.file = request.FILES["file"]
            task.save()
            return redirect(
                reverse(
                    "handle-task-v1", kwargs={"list_id": list_id, "task_id": task_id}
                )
            )
        else:
            ValidationError("invalid data")
    return render(request, "non-model-edit-task.html", context={"form": form})
