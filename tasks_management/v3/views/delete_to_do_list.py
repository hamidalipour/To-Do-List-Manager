from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import FormView

from tasks_management import forms
from tasks_management.models import ToDoList


class DeleteToDoListView(LoginRequiredMixin, FormView):
    form_class = forms.EmptyForm
    token = None

    def form_valid(self, form):
        to_do_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        to_do_list.delete()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("to-do-lists-page-v3")
