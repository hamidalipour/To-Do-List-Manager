from django.urls import include, path
from rest_framework import routers

from tasks_management.v6 import views

router = routers.DefaultRouter()
router.register("to-do-lists", views.ToDoListsView, basename="to-do-lists-v6")
router.register("tasks", views.TasksView, basename="tasks-v6")
router.register("tokens", views.TokensView, basename="tokens-v6")


urlpatterns = [
    path("", include(router.urls)),
]
