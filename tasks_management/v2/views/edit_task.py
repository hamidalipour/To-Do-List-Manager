from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from tasks_management import forms
from tasks_management.models import Task


class EditTaskView(View):
    def get(self, request, task_id, list_id):
        task = Task.objects.get(id=task_id)
        form = forms.TaskForm(instance=task)
        return render(request, "edit-task.html", context={"form": form})

    def post(self, request, list_id, task_id):
        task = Task.objects.get(id=task_id)
        form = forms.TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect(
                reverse(
                    "handle-task-v2", kwargs={"list_id": list_id, "task_id": task_id}
                )
            )
        else:
            ValidationError("invalid data")
            return render(request, "edit-task.html", context={"form": form})
