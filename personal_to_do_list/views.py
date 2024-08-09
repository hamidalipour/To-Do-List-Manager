from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from personal_to_do_list import forms


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
                message = 'Incorrect username or password'
    return render(
        request, 'login.html', context={'form': form, 'message': message})


def logout_page(request):
    logout(request)
    return redirect('login')


def home_page(request):
    user = request.user
    return render(request, 'home-page.html', context={'user': user})
