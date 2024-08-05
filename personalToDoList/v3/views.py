from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from personalToDoList import forms
from personalToDoList.models import ToDoList, Task, Token
from django.views import View
from django.conf import settings
from django.views.generic.list import ListView
from django.views.generic import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

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


# class TasksPageView(LoginRequiredMixin, ListView, CreateView):
#     model = Task
#     template_name = 'tasks.html'
#     form_class = forms.TokenForm
#     list_id = None
#     message = ''
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['tasks'] = self.object_list.filter(toDoList__id=self.kwargs['list_id']).order_by('due_date',
#                                                                                                  '-is_priority')
#         self.success_url = f"{DEFAULT_DOMAIN}v3/to-do-lists/{self.kwargs['list_id']}/"
#         context['default_domain'] = DEFAULT_DOMAIN
#         context['version'] = "v3"
#         context['message'] = self.message
#         context['form'] = self.get_form()
#         self.list_id = self.kwargs['list_id']
#         context['list_id'] = self.kwargs['list_id']
#         return context
#
#     def form_valid(self, form):
#         uuid = self.form_class.cleaned_data['uuid']
#         try:
#             token = Token.objects.get(uuid=uuid)
#             to_do_list = ToDoList.objects.get(id=self.list_id)
#             token.task.toDoLists.add(to_do_list)
#             self.message = "task has been added"
#         except ValidationError:
#             self.message = "invalid token format"
#         except Token.DoesNotExist:
#             self.message = "token doesn't exist"
#
#         return super().form_valid(form)


class TasksPageView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks.html'
    message = ''
    list_id = None


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(toDoLists__id=self.kwargs['list_id']).order_by('due_date', '-is_priority')
        context['default_domain'] = DEFAULT_DOMAIN
        context['version'] = "v3"
        context['message'] = self.message
        context['form'] = forms.TokenForm
        self.list_id = self.kwargs['list_id']
        context['list_id'] = self.kwargs['list_id']
        return context

class CreateTaskWithUUIDView(LoginRequiredMixin, FormView):
    form_class = forms.TokenForm
    template_name = 'tasks.html'
    message = ''

    def form_valid(self, form):

        uuid = form.cleaned_data['uuid']
        try:
            token = Token.objects.get(uuid=uuid)
            to_do_list = ToDoList.objects.get(id=self.kwargs['list_id'])
            token.task.toDoLists.add(to_do_list)
            self.message = "task has been added"
        except ValidationError:
            self.message = "invalid token format"
        except Token.DoesNotExist:
            self.message = "token doesn't exist"

        return super().form_valid(form)

    def get_success_url(self):
        return f"{DEFAULT_DOMAIN}v3/to-do-lists/{self.kwargs['list_id']}/"




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
