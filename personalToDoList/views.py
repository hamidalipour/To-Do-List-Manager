# authentication/views.py
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from . import forms
from django.contrib.auth import login, authenticate
from personalToDoList.models import ToDoList, Task, Token


def check_user_authentication(user):
    pass


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Hello {user.username}! You have been logged in'
            else:
                message = 'Login failed!'
    return render(
        request, 'login.html', context={'form': form, 'message': message})


def to_do_lists_page(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("http://localhost:8000/admin")
    else:
        to_do_lists = ToDoList.objects.filter(user=user)
        return render(request, 'to_do_list_page.html', context={'to_do_lists': to_do_lists})


def tasks_page(request, list_id):
    if not request.user.is_authenticated:
        return redirect("http://localhost:8000/admin")
    else:
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
                except ValidationError:
                    message = "invalid token format"
                except Token.DoesNotExist:
                    message = "token doesn't exist"

        return render(
            request, 'tasks.html', context={'tasks': tasks, 'list_id': list_id, 'form': form, 'message': message})


def create_to_do_list(request):
    if not request.user.is_authenticated:
        return redirect("http://localhost:8000/admin")
    form = forms.ToDoListForm()
    if request.method == 'POST':
        form = forms.ToDoListForm(request.POST)
        if form.is_valid():
            _list = form.save(commit=False)
            _list.user = request.user
            _list.save()
            return redirect("http://localhost:8000/to-do-lists")
        else:
            return redirect("http://localhost:8000/create-to-do-list/")
    return render(request, 'create_to_do_list.html', context={'form': form})


def create_task(request, list_id):
    if not request.user.is_authenticated:
        return redirect("http://localhost:8000/admin")
    form = forms.TaskForm()
    if request.method == 'POST':
        form = forms.TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            task.toDoLists.add(ToDoList.objects.get(id=list_id))
            return redirect(f"http://localhost:8000/to-do-lists/{list_id}")
        else:
            return redirect("http://localhost:8000/create-tasks/")
    return render(request, 'create_task.html', context={'form': form})


def handle_task(request, task_id):
    if not request.user.is_authenticated:
        return redirect("http://localhost:8000/admin")
    else:
        token = None
        task = Task.objects.get(id=task_id)
        if request.method == 'POST':
            token = Token.objects.create(task=task)
        return render(request, 'handle-task.html', context={'task': task, 'token': token})
