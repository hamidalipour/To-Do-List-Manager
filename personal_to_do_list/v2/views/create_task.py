from django.shortcuts import render, redirect
from django.views import View

from personal_to_do_list import forms
from personal_to_do_list.models import ToDoList
from django.conf import settings

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


class CreateTaskView(View):
    def get(self, request, list_id):
        form = forms.TaskForm()
        return render(request, 'create-task.html', context={'form': form})

    def post(self, request, list_id):
        form = forms.TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            task.to_do_lists.add(ToDoList.objects.get(id=list_id))
            return redirect(f"{DEFAULT_DOMAIN}v2/to-do-lists/{list_id}")
        else:
            return redirect(f"{DEFAULT_DOMAIN}v2/create-task/")
