from django import forms

from personalToDoList.models import ToDoList, Task, Token


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
