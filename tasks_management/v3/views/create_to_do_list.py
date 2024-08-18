from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView

from tasks_management import forms
from tasks_management.models import ToDoList


class CreateToDoListView(LoginRequiredMixin, CreateView):
    model = ToDoList
    template_name = "create-to-do-list.html"
    form_class = forms.ToDoListForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        ValidationError("invalid data")
        return render(self.request, "create-task.html", context={"form": form})

    def get_success_url(self):
        return reverse("to-do-lists-page-v3")
