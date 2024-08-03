from django import forms

from personalToDoList.models import ToDoList


class LoginForm(forms.Form):
    username = forms.CharField(max_length=70)
    password = forms.CharField(max_length=70, widget=forms.PasswordInput)


class ToDoListForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ('title',)
