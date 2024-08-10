from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from personal_to_do_list import forms
from personal_to_do_list.models import ToDoList

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


class CreateToDoListView(LoginRequiredMixin, CreateView):
    model = ToDoList
    template_name = 'create-to-do-list.html'
    form_class = forms.ToDoListForm
    success_url = f"{DEFAULT_DOMAIN}v3/to-do-lists"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
