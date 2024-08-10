from django.conf import settings
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views import View

from personal_to_do_list import forms
from personal_to_do_list.models import Task, Token, ToDoList

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


class TasksPageView(View):
    def get(self, request, list_id):
        tasks = Task.objects.filter(to_do_lists__id=list_id).order_by('due_date', '-is_priority')
        form = forms.TokenForm()
        message = ''
        version = "v2"
        return render(
            request, 'tasks.html', context={'tasks': tasks, 'list_id': list_id, 'form': form, 'message': message,
                                            'version': version, 'default_domain': DEFAULT_DOMAIN})

    def post(self, request, list_id):
        tasks = Task.objects.filter(to_do_lists__id=list_id).order_by('due_date', '-is_priority')
        message = ''
        form = forms.TokenForm(request.POST)
        version = "v2"
        if form.is_valid():
            uuid = form.cleaned_data['uuid']
            try:
                token = Token.objects.get(uuid=uuid)
                to_do_list = ToDoList.objects.get(id=list_id)
                token.task.to_do_lists.add(to_do_list)
                message = "task has been added"
            except ValidationError:
                message = "invalid token format"
            except Token.DoesNotExist:
                message = "token doesn't exist"
        return render(
            request, 'tasks.html', context={'tasks': tasks, 'list_id': list_id, 'form': form, 'message': message,
                                            'version': version, 'default_domain': DEFAULT_DOMAIN})
