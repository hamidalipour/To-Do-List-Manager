from django.contrib import admin

from tasks_management.models import Task, ToDoList, Token

admin.site.register(Task)
admin.site.register(ToDoList)
admin.site.register(Token)
