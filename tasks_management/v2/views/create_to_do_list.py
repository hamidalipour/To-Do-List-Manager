from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from tasks_management import forms


class CreateToDoListView(View):
    def get(self, request):
        form = forms.ToDoListForm()
        return render(request, "create-to-do-list.html", context={"form": form})

    def post(self, request):
        form = forms.ToDoListForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect(reverse("to-do-lists-page-v2"))
        else:
            ValidationError("invalid data")
            return render(request, "create-to-do-list.html", context={"form": form})
