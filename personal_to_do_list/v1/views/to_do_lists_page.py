from django.shortcuts import render

from personal_to_do_list.models import ToDoList
from django.conf import settings

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


def to_do_lists_page(request):
    user = request.user
    version = "v1"
    to_do_lists = ToDoList.objects.filter(user=user)
    return render(request, 'to-do-list-page.html',
                  context={'to_do_lists': to_do_lists, 'version': version, 'default_domain': DEFAULT_DOMAIN})

