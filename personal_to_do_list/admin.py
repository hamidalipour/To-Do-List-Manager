from django.contrib import admin

from personal_to_do_list.models import ToDoList
from personal_to_do_list.models import Task
from personal_to_do_list.models import Token

admin.site.register(Task)
admin.site.register(ToDoList)
admin.site.register(Token)
