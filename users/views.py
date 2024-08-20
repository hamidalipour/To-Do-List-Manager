from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

from tasks_management import forms


def login_page(request):
    if request.user.is_authenticated:
        return redirect(reverse("home-page"))
    form = forms.LoginForm()
    message = ""
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                message = f"Hello {user.username}! You have been logged in"
                return redirect(reverse("home-page"))
            else:
                message = "Incorrect username or password"
    return render(request, "login.html", context={"form": form, "message": message})


def logout_page(request):
    logout(request)
    return redirect("login")


def home_page(request):
    user = request.user
    if request.method == "POST":
        if "v1" in request.POST:
            return redirect(reverse("to-do-lists-page-v1"))
        elif "v2" in request.POST:
            return redirect(reverse("to-do-lists-page-v2"))
        elif "v3" in request.POST:
            return redirect(reverse("to-do-lists-page-v3"))
        elif "v4" in request.POST:
            return redirect(reverse("to-do-lists-page-v4"))
        elif "v5" in request.POST:
            return redirect(reverse("to-do-lists-page-v5"))
        elif "v6" in request.POST:
            return redirect(reverse("to-do-lists-v6-list"))
    return render(request, "home-page.html", context={"user": user})


def default(request):
    return redirect(reverse("home-page"))
