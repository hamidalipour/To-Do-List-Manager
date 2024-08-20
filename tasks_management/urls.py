from django.urls import include, path

urlpatterns = [
    path("v1/", include("tasks_management.v1.urls")),
    path("v2/", include("tasks_management.v2.urls")),
    path("v3/", include("tasks_management.v3.urls")),
    path("v4/", include("tasks_management.v4.urls")),
    path("v5/", include("tasks_management.v5.urls")),
    path("v6/", include("tasks_management.v6.urls")),
]
