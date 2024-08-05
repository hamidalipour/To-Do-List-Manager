from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from personalToDoList import forms
from personalToDoList.models import ToDoList, Task, Token
from django.views import View
from django.conf import settings

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


class BaseView(View):
    def check_authentication(self, request):
        if request.user.is_authenticated:
            return True
        return False


class ToDoListsPageView(BaseView):
    def get(self, request):
        if not self.check_authentication(request):
            return redirect(f"{DEFAULT_DOMAIN}admin")
        version = "v2"
        to_do_lists = ToDoList.objects.filter(user=request.user)
        return render(request, 'to-do-list-page.html',
                      context={'to_do_lists': to_do_lists, 'version': version, 'default_domain': DEFAULT_DOMAIN})


class TasksPageView(BaseView):
    def get(self, request, list_id):
        if not self.check_authentication(request):
            return redirect(f"{DEFAULT_DOMAIN}admin")
        tasks = Task.objects.filter(toDoLists__id=list_id).order_by('due_date', '-is_priority')
        form = forms.TokenForm()
        message = ''
        version = "v2"
        return render(
            request, 'tasks.html', context={'tasks': tasks, 'list_id': list_id, 'form': form, 'message': message,
                                            'version': version, 'default_domain': DEFAULT_DOMAIN})

    def post(self, request, list_id):
        if not self.check_authentication(request):
            return redirect(f"{DEFAULT_DOMAIN}admin")
        tasks = Task.objects.filter(toDoLists__id=list_id).order_by('due_date', '-is_priority')
        message = ''
        form = forms.TokenForm(request.POST)
        version = "v2"
        if form.is_valid():
            uuid = form.cleaned_data['uuid']
            try:
                token = Token.objects.get(uuid=uuid)
                to_do_list = ToDoList.objects.get(id=list_id)
                token.task.toDoLists.add(to_do_list)
                message = "task has been added"
            except ValidationError:
                message = "invalid token format"
            except Token.DoesNotExist:
                message = "token doesn't exist"
        return render(
            request, 'tasks.html', context={'tasks': tasks, 'list_id': list_id, 'form': form, 'message': message,
                                            'version': version, 'default_domain': DEFAULT_DOMAIN})


class CreateToDoListView(BaseView):
    def get(self, request):
        if not self.check_authentication(request):
            return redirect(f"{DEFAULT_DOMAIN}admin")
        form = forms.ToDoListForm()
        return render(request, 'create-to-do-list.html', context={'form': form})

    def post(self, request):
        if not self.check_authentication(request):
            return redirect(f"{DEFAULT_DOMAIN}admin")
        form = forms.ToDoListForm(request.POST)
        if form.is_valid():
            _list = form.save(commit=False)
            _list.user = request.user
            _list.save()
            return redirect(f"{DEFAULT_DOMAIN}v2/to-do-lists")
        else:
            return redirect(f"{DEFAULT_DOMAIN}v2/create-to-do-list/")


class CreateTaskView(BaseView):
    def get(self, request, list_id):
        if not self.check_authentication(request):
            return redirect(f"{DEFAULT_DOMAIN}admin")
        form = forms.TaskForm()
        return render(request, 'create-task.html', context={'form': form})

    def post(self, request, list_id):
        if not self.check_authentication(request):
            return redirect(f"{DEFAULT_DOMAIN}admin")
        form = forms.TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            task.toDoLists.add(ToDoList.objects.get(id=list_id))
            return redirect(f"{DEFAULT_DOMAIN}v2/to-do-lists/{list_id}")
        else:
            return redirect(f"{DEFAULT_DOMAIN}v2/create-task/")


class HandleTaskView(BaseView):
    def get(self, request, task_id):
        if not self.check_authentication(request):
            return redirect(f"{DEFAULT_DOMAIN}admin")
        token = None
        task = Task.objects.get(id=task_id)
        return render(request, 'handle-task.html', context={'task': task, 'token': token})

    def post(self, request, task_id):
        if not self.check_authentication(request):
            return redirect(f"{DEFAULT_DOMAIN}admin")
        task = Task.objects.get(id=task_id)
        token = Token.objects.create(task=task)
        return render(request, 'handle-task.html', context={'task': task, 'token': token})
