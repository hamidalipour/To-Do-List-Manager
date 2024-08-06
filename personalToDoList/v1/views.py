from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from personalToDoList import forms
from personalToDoList.models import ToDoList, Task, Token
from django.conf import settings

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


# def check_user_authentication(user):
#     pass


# def login_page(request):
#     form = forms.LoginForm()
#     message = ''
#     if request.method == 'POST':
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             user = authenticate(
#                 username=form.cleaned_data['username'],
#                 password=form.cleaned_data['password'],
#             )
#             if user is not None:
#                 login(request, user)
#                 message = f'Hello {user.username}! You have been logged in'
#             else:
#                 message = 'Login failed!'
#     return render(
#         request, 'login.html', context={'form': form, 'message': message})


def to_do_lists_page(request):
    user = request.user
    version = "v1"
    to_do_lists = ToDoList.objects.filter(user=user)
    return render(request, 'to-do-list-page.html',
                  context={'to_do_lists': to_do_lists, 'version': version, 'default_domain': DEFAULT_DOMAIN})


def tasks_page(request, list_id):
    version = "v1"
    tasks = Task.objects.filter(toDoLists__id=list_id).order_by('due_date', '-is_priority')
    form = forms.TokenForm()
    message = ''
    if request.method == 'POST':
        form = forms.TokenForm(request.POST)
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

    return render(request, 'tasks.html',
                  context={'tasks': tasks, 'list_id': list_id, 'form': form, 'message': message, 'version': version, 'default_domain': DEFAULT_DOMAIN})


def create_to_do_list(request):
    form = forms.ToDoListForm()
    if request.method == 'POST':
        form = forms.ToDoListForm(request.POST)
        if form.is_valid():
            _list = form.save(commit=False)
            _list.user = request.user
            _list.save()
            return redirect(f"{DEFAULT_DOMAIN}v1/to-do-lists")
        else:
            return redirect(f"{DEFAULT_DOMAIN}v1/create-to-do-list/")
    return render(request, 'create-to-do-list.html', context={'form': form})


def create_task(request, list_id):
    form = forms.TaskForm()
    if request.method == 'POST':
        form = forms.TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            task.toDoLists.add(ToDoList.objects.get(id=list_id))
            return redirect(f"{DEFAULT_DOMAIN}v1/to-do-lists/{list_id}")
        else:
            return redirect(f"{DEFAULT_DOMAIN}v1/create-tasks/")
    return render(request, 'create-task.html', context={'form': form})


def handle_task(request, task_id):
    token = None
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        token = Token.objects.create(task=task)
        token = token.uuid
    return render(request, 'handle-task.html',
                  context={'task': task, 'token': token, 'version': "v1", 'default_domain': DEFAULT_DOMAIN})
