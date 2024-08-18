from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse

from tasks_management.models import ToDoList
from tasks_management.v1 import non_model_forms


def create_to_do_list(request):
    form = non_model_forms.ToDoListForm()
    if request.method == "POST":
        form = non_model_forms.ToDoListForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            ToDoList.objects.create(title=title, user=request.user)
            return redirect(reverse("to-do-lists-page-v1"))
        else:
            ValidationError("invalid data")
    return render(request, "non-model-create-to-do-list.html", context={"form": form})
