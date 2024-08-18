from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import FormView

from tasks_management import forms
from tasks_management.models import Task, ToDoList


class DeleteTaskView(LoginRequiredMixin, FormView):
    form_class = forms.EmptyForm

    def form_valid(self, form):
        task = Task.objects.get(id=self.kwargs["task_id"])
        to_do_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        task.to_do_lists.remove(to_do_list)
        if not task.to_do_lists.exists():
            task.delete()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tasks-page-v3", kwargs={"list_id": self.kwargs["list_id"]})
