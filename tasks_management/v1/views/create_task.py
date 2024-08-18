from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse

from tasks_management.models import Task, ToDoList
from tasks_management.v1 import non_model_forms


def create_task(request, list_id):
    form = non_model_forms.TaskForm()
    if request.method == "POST":
        form = non_model_forms.TaskForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            done = form.cleaned_data["done"]
            due_date = form.cleaned_data["due_date"]
            priority = form.cleaned_data["priority"]
            file = request.FILES["file"]
            task = Task.objects.create(
                title=title,
                description=description,
                done=done,
                due_date=due_date,
                priority=priority,
                file=file,
            )
            task.to_do_lists.add(ToDoList.objects.get(id=list_id))
            return redirect(reverse("tasks-page-v1", kwargs={"list_id": list_id}))
        else:
            ValidationError("invalid data")
    return render(request, "non-model-create-task.html", context={"form": form})
