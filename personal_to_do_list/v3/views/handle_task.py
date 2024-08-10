from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from personal_to_do_list import forms
from personal_to_do_list.models import Task, ToDoList, Token

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


class HandleTaskView(TemplateView):
    template_name = 'handle-task.html'
    token = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = Task.objects.get(id=self.kwargs['task_id'])
        context['task'] = task
        self.token = self.request.GET.get('uuid')
        context['token'] = self.token
        context['version'] = "v3"
        context['default_domain'] = DEFAULT_DOMAIN
        return context


class CreateUUIDView(LoginRequiredMixin, FormView):
    form_class = forms.EmptyForm
    template_name = 'handle-task.html'
    token = None

    def form_valid(self, form):
        task = Task.objects.get(id=self.kwargs['task_id'])
        self.token = Token.objects.create(task=task)
        return super().form_valid(form)

    def get_success_url(self):
        return f"{reverse('handle-task-v3', kwargs={'task_id': self.kwargs['task_id'], 'list_id': self.kwargs['list_id']})}?uuid={self.token.uuid}"
