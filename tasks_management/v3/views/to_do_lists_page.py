from django.conf import settings
from django.urls import reverse
from django.views.generic import ListView

from tasks_management.models import ToDoList

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


class ToDoListsPageView(ListView):
    model = ToDoList
    template_name = "to-do-list-page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["to_do_lists"] = self.object_list.filter(user=self.request.user)
        context["default_url"] = f"{DEFAULT_DOMAIN}v3"
        context["create_to_do_list_url"] = reverse("create-to-do-list-v3")
        return context
