from django.contrib import admin

from personalToDoList.models import ToDoList
from personalToDoList.models import Task
from personalToDoList.models import Token

admin.site.register(Task)
admin.site.register(ToDoList)
admin.site.register(Token)
