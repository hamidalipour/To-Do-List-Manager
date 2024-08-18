from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from tasks_management import forms
from tasks_management.models import Task, Token


class HandleTaskView(TemplateView):
    template_name = "handle-task.html"
    token = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = Task.objects.get(id=self.kwargs["task_id"])
        context["task"] = task
        self.token = self.request.GET.get("uuid")
        context["token"] = self.token
        context["create_url"] = reverse(
            "create-uuid-v3",
            kwargs={
                "list_id": self.kwargs["list_id"],
                "task_id": self.kwargs["task_id"],
            },
        )
        context["delete_url"] = reverse(
            "delete-task-v3",
            kwargs={
                "list_id": self.kwargs["list_id"],
                "task_id": self.kwargs["task_id"],
            },
        )
        context["edit_url"] = reverse(
            "edit-task-v3",
            kwargs={
                "list_id": self.kwargs["list_id"],
                "task_id": self.kwargs["task_id"],
            },
        )
        return context


class CreateUUIDView(LoginRequiredMixin, FormView):
    form_class = forms.EmptyForm
    template_name = "handle-task.html"
    token = None

    def form_valid(self, form):
        task = Task.objects.get(id=self.kwargs["task_id"])
        self.token = Token.objects.create(task=task)
        return super().form_valid(form)

    def get_success_url(self):
        return f"{reverse('handle-task-v3', kwargs={'task_id': self.kwargs['task_id'], 'list_id': self.kwargs['list_id']})}?uuid={self.token.uuid}"
