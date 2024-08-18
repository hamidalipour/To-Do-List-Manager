from django.urls import reverse
from django.views.generic import UpdateView

from tasks_management.models import Task


class EditTaskView(UpdateView):
    model = Task
    fields = ["title", "description", "done", "due_date", "priority", "file"]
    template_name = "edit-task.html"
    context_object_name = "task"

    def get_success_url(self):
        return reverse(
            "handle-task-v3",
            kwargs={
                "list_id": self.kwargs["list_id"],
                "task_id": self.kwargs["task_id"],
            },
        )

    def get_object(self, queryset=None):
        return Task.objects.get(id=self.kwargs["task_id"])
