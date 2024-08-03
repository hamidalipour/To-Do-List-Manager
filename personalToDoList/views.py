# authentication/views.py
from django.shortcuts import render, redirect

from . import forms
from django.contrib.auth import login, authenticate
from personalToDoList.models import ToDoList


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
    # form = forms.ToDoListForm()
    user = request.user
    if not user.is_authenticated:
        return redirect("http://localhost:8000/admin")
    else:
        to_do_lists = ToDoList.objects.filter(user=user)
        url = "http://localhost:8000"
        return render(request, 'to_do_list_page.html', context={'to_do_lists': to_do_lists})


def tasks_page(request, list_id):
    return render(request, 'base.html')


def create_to_do_list(request):
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
