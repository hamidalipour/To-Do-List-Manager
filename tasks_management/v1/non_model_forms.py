from django import forms
from django.utils import timezone

from tasks_management.validators import validate_date

PRIORITY = (
    ("High", "High"),
    ("Medium", "Medium"),
    ("Low", "Low"),
)


class ToDoListForm(forms.Form):
    title = forms.CharField(max_length=100)


class TaskForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(required=False, widget=forms.Textarea)
    done = forms.BooleanField(required=False)
    due_date = forms.DateField(initial=timezone.now(), validators=[validate_date])
    priority = forms.ChoiceField(choices=PRIORITY)
    file = forms.FileField(required=False)
