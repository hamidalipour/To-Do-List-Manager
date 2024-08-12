from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from personal_to_do_list import forms
from personal_to_do_list.models import Task, ToDoList

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


class CreateTaskView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "create-task.html"
    form_class = forms.TaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def get_success_url(self):
        return f"{DEFAULT_DOMAIN}v3/to-do-lists/{self.kwargs['list_id']}/"

    def form_valid(self, form):
        form.save()
        form.instance.to_do_lists.add(ToDoList.objects.get(id=self.kwargs["list_id"]))
        return super().form_valid(form)
