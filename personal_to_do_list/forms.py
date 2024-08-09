from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from personal_to_do_list.models import ToDoList, Task, Token


class LoginForm(forms.Form):
    username = forms.CharField(max_length=70)
    password = forms.CharField(max_length=70, widget=forms.PasswordInput)


class ToDoListForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ('title',)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'done', 'due_date', 'is_priority')


class TokenForm(forms.Form):
    uuid = forms.CharField(label="enter uuid")


class EmptyForm(forms.Form):
    pass


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password')