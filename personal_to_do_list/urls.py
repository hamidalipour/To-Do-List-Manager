from django.urls import path, include

urlpatterns = [
    path("v1/", include("personal_to_do_list.v1.urls")),
    path("v2/", include("personal_to_do_list.v2.urls")),
    path("v3/", include("personal_to_do_list.v3.urls")),
]
