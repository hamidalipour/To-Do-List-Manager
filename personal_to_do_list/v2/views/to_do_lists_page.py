from django.shortcuts import render
from django.views import View

from personal_to_do_list.models import ToDoList
from django.conf import settings

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


class ToDoListsPageView(View):
    def get(self, request):
        version = "v2"
        to_do_lists = ToDoList.objects.filter(user=request.user)
        return render(
            request,
            "to-do-list-page.html",
            context={
                "to_do_lists": to_do_lists,
                "version": version,
                "default_domain": DEFAULT_DOMAIN,
            },
        )
