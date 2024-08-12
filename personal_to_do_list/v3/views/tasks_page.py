from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.views.generic import ListView, FormView

from personal_to_do_list import forms
from personal_to_do_list.models import Task, Token, ToDoList
from django.conf import settings

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


class TasksPageView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks.html"
    message = ""
    list_id = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.filter(
            to_do_lists__id=self.kwargs["list_id"]
        ).order_by("due_date", "-is_priority")
        context["default_domain"] = DEFAULT_DOMAIN
        context["version"] = "v3"
        context["message"] = self.request.GET.get("message")
        context["form"] = forms.TokenForm
        self.list_id = self.kwargs["list_id"]
        context["list_id"] = self.kwargs["list_id"]
        return context


class CreateTaskWithUUIDView(LoginRequiredMixin, FormView):
    form_class = forms.TokenForm
    template_name = "tasks.html"
    message = ""

    def form_valid(self, form):
        uuid = form.cleaned_data["uuid"]
        try:
            token = Token.objects.get(uuid=uuid)
            to_do_list = ToDoList.objects.get(id=self.kwargs["list_id"])
            token.task.to_do_lists.add(to_do_list)
            self.message = "task has been added"
        except ValidationError:
            self.message = "invalid token format"
        except Token.DoesNotExist:
            self.message = "token doesn't exist"

        return super().form_valid(form)

    def get_success_url(self):
        return f"{reverse('tasks-page-v3', kwargs={'list_id': self.kwargs['list_id']})}?message={self.message}"
