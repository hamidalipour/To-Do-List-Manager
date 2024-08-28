from django.conf import settings
from django.shortcuts import redirect
from tasks_management.tasks import change_tasks

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


def login_middleware(get_response):
    def middleware(request):
        # change_tasks.delay()
        if request.user.is_authenticated:
            response = get_response(request)
            return response
        if request.path.startswith("/admin") or request.path.startswith("/login"):
            response = get_response(request)
            return response

        return redirect(f"{DEFAULT_DOMAIN}login")

    return middleware
