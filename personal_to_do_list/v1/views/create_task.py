from django.shortcuts import redirect, render

from personal_to_do_list import forms
from personal_to_do_list.models import ToDoList
from django.conf import settings

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


def create_task(request, list_id):
    form = forms.TaskForm()
    if request.method == 'POST':
        form = forms.TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            task.to_do_lists.add(ToDoList.objects.get(id=list_id))
            return redirect(f"{DEFAULT_DOMAIN}v1/to-do-lists/{list_id}")
        else:
            return redirect(f"{DEFAULT_DOMAIN}v1/create-tasks/")
    return render(request, 'create-task.html', context={'form': form})
