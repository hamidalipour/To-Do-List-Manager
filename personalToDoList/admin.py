from django.contrib import admin

from personalToDoList.models import ToDoList
from personalToDoList.models import Task

admin.site.register(Task)
admin.site.register(ToDoList)
