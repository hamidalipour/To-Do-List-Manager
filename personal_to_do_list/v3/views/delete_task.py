from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from personal_to_do_list import forms
from personal_to_do_list.models import Task, ToDoList

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


class DeleteTaskView(LoginRequiredMixin, FormView):
    form_class = forms.EmptyForm
    token = None

    def form_valid(self, form):
        task = Task.objects.get(id=self.kwargs["task_id"])
        to_do_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        task.to_do_lists.remove(to_do_list)
        if not task.to_do_lists.exists():
            task.delete()
        return super().form_valid(form)

    def get_success_url(self):
        return f"{DEFAULT_DOMAIN}v3/to-do-lists/{self.kwargs['list_id']}"
