from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Case, Value, When
from django.urls import reverse
from django.views.generic import FormView, ListView

from tasks_management import forms
from tasks_management.models import Task, ToDoList, Token

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


class TasksPageView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks.html"
    message = ""
    list_id = None
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        priority_order = Case(
            When(priority=Task.Priority.HIGH, then=Value(1)),
            When(priority=Task.Priority.MEDIUM, then=Value(2)),
            When(priority=Task.Priority.LOW, then=Value(3)),
        )
        context["tasks"] = (
            Task.objects.filter(to_do_lists__id=self.kwargs["list_id"])
            .annotate(priority_order=priority_order)
            .order_by("due_date", "priority_order")
        )
        context["default_url"] = f"{DEFAULT_DOMAIN}v3"
        context["create_task_url"] = reverse(
            "create-task-v3", kwargs={"list_id": self.kwargs["list_id"]}
        )
        context["create_with_uuid_url"] = reverse(
            "create-task-with-uuid-v3", kwargs={"list_id": self.kwargs["list_id"]}
        )
        context["delete_to_do_list_url"] = reverse(
            "delete-to-do-list-v3", kwargs={"list_id": self.kwargs["list_id"]}
        )
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
