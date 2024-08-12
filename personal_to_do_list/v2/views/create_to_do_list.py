from django.shortcuts import render, redirect
from django.views import View

from personal_to_do_list import forms
from django.conf import settings

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


class CreateToDoListView(View):
    def get(self, request):
        form = forms.ToDoListForm()
        return render(request, "create-to-do-list.html", context={"form": form})

    def post(self, request):
        form = forms.ToDoListForm(request.POST)
        if form.is_valid():
            _list = form.save(commit=False)
            _list.user = request.user
            _list.save()
            return redirect(f"{DEFAULT_DOMAIN}v2/to-do-lists")
        else:
            return redirect(f"{DEFAULT_DOMAIN}v2/create-to-do-list/")
