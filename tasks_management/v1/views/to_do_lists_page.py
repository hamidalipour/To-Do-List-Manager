from django.conf import settings
from django.shortcuts import render
from django.urls import reverse

from tasks_management.models import ToDoList

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


def to_do_lists_page(request):
    user = request.user
    to_do_lists = ToDoList.objects.filter(user=user)
    default_url = f"{DEFAULT_DOMAIN}v1"
    create_to_do_list_url = reverse("create-to-do-list-v1")
    return render(
        request,
        "to-do-list-page.html",
        context={
            "to_do_lists": to_do_lists,
            "default_url": default_url,
            "create_to_do_list_url": create_to_do_list_url,
        },
    )
