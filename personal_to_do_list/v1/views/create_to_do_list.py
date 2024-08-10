from django.conf import settings
from django.shortcuts import redirect, render

from personal_to_do_list import forms

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


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
