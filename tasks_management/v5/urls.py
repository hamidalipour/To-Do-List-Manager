from django.urls import include, path
from rest_framework import routers

from tasks_management.v5 import views

router = routers.DefaultRouter()
# router.register(r'to-do-lists', views.ToDoListsView, basename='to-do-lists-page-v5')
# router.register(r'create-to-do-list', views.CreateToDoListView, basename='create-to-do-list-v5')

urlpatterns = [
    path('', include(router.urls)),
    path('to-do-lists', views.ToDoListsView.as_view({'get': 'list'}), name='to-do-lists-page-v5'),
    path('create-to-do-list', views.ToDoListsView.as_view({'post': 'create'}), name='create-to-do-list-v5'),
    path(
        "delete-to-do-list/<int:list_id>",
        views.ToDoListsView.as_view({'delete': 'destroy'}),
        name="delete-to-do-list-v5",
    ),
    path(
        "to-do-lists/<int:list_id>",
        views.TasksView.as_view({'get': 'list'}),
        name="tasks-page-v5",
    ),
    path("create-task/<int:list_id>", views.TasksView.as_view({'post': 'create'}), name="create-task-v5"),
    path(
        "delete-task/<int:task_id>/<int:list_id>",
        views.TasksView.as_view({'delete': 'destroy'}),
        name="delete-task-v5",
    ),
    path(
        "edit-task/<int:task_id>",
        views.TasksView.as_view({'post': 'update'}),
        name="edit-task-v5",
    ),
    path(
        "create-uuid/<int:task_id>",
        views.TokenView.as_view({'post': 'create'}),
        name="create-uuid-v5",
    ),
    path(
        "create-task-with-uuid/<int:list_id>",
        views.TaskWithUuid.as_view({'post': 'create'}),
        name="create-task-with-uuid-v5",
    ),


]