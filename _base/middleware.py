from django.conf import settings
from django.shortcuts import redirect

DEFAULT_DOMAIN = settings.DEFAULT_DOMAIN


def login_middleware(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            response = get_response(request)
            return response
        if request.path.startswith("/admin") or request.path.startswith("/login"):
            response = get_response(request)
            return response

        return redirect(f"{DEFAULT_DOMAIN}login")

    return middleware
