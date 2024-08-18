from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from tasks_management.models import ToDoList

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


class ToDoListsPageView(View):
    def get(self, request):
        to_do_lists = ToDoList.objects.filter(user=request.user)
        default_url = f"{DEFAULT_DOMAIN}v2"
        create_to_do_list_url = reverse("create-to-do-list-v2")
        return render(
            request,
            "to-do-list-page.html",
            context={
                "to_do_lists": to_do_lists,
                "default_url": default_url,
                "create_to_do_list_url": create_to_do_list_url,
            },
        )
