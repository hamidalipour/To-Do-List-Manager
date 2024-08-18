from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from tasks_management import forms
from tasks_management.models import ToDoList


class CreateTaskView(View):
    def get(self, request, list_id):
        form = forms.TaskForm()
        return render(request, "create-task.html", context={"form": form})

    def post(self, request, list_id):
        form = forms.TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save()
            task.to_do_lists.add(ToDoList.objects.get(id=list_id))
            return redirect(reverse("tasks-page-v2", kwargs={"list_id": list_id}))
        else:
            ValidationError("invalid data")
            return render(request, "create-task.html", context={"form": form})
