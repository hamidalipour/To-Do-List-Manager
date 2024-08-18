from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView

from tasks_management import forms
from tasks_management.models import Task, ToDoList


class CreateTaskView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "create-task.html"
    form_class = forms.TaskForm
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def get_success_url(self):
        return reverse("tasks-page-v3", kwargs={"list_id": self.kwargs["list_id"]})

    def form_valid(self, form):
        form.save()
        form.instance.to_do_lists.add(ToDoList.objects.get(id=self.kwargs["list_id"]))
        return super().form_valid(form)

    def form_invalid(self, form):
        ValidationError("invalid data")
        return render(self.request, "create-task.html", context={"form": form})
