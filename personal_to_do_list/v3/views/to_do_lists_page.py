from django.views.generic import ListView

from personal_to_do_list.models import ToDoList
from django.conf import settings

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


class ToDoListsPageView(ListView):
    model = ToDoList
    template_name = 'to-do-list-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['to_do_lists'] = self.object_list.filter(user=self.request.user)
        context['version'] = "v3"
        context['default_domain'] = DEFAULT_DOMAIN
        return context
