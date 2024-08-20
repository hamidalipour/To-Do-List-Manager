from django.urls import include, path
from rest_framework import routers

from tasks_management.v4 import views

router = routers.DefaultRouter()
# router.register(r'temp', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('to-do-lists', views.ToDoListsView.as_view(), name='to-do-lists-page-v4'),
    path('create-to-do-list', views.CreateToDoListView.as_view(), name='create-to-do-list-v4'),
    path(
        "to-do-lists/<int:list_id>",
        views.TasksView.as_view(),
        name="tasks-page-v4",
    ),
    path("create-task/<int:list_id>", views.CreateTask.as_view(), name="create-task-v4"),
    path(
        "delete-to-do-list/<int:list_id>",
        views.DeleteToDoListView.as_view(),
        name="delete-to-do-list-v4",
    ),
    path(
        "create-task-with-uuid/<int:list_id>",
        views.CreateTaskWithUuidView.as_view(),
        name="create-task-with-uuid-v4",
    ),
    path(
        "delete-task/<int:task_id>/<int:list_id>",
        views.DeleteTaskView.as_view(),
        name="delete-task-v4",
    ),
    path(
        "create-uuid/<int:task_id>",
        views.CreateUuidView.as_view(),
        name="create-uuid-v4",
    ),
    path(
        "edit-task/<int:task_id>",
        views.EditTaskView.as_view(),
        name="edit-task-v4",
    ),
]