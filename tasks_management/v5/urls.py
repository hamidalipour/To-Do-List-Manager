from django.urls import include, path
from rest_framework import routers

from tasks_management.v5 import views

router = routers.DefaultRouter()
# router.register(r'to-do-lists', views.ToDoListsView, basename='to-do-lists-page-v5')
# router.register(r'create-to-do-list', views.CreateToDoListView, basename='create-to-do-list-v5')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('to-do-lists', views.ToDoListsView.as_view({'get': 'list'}), name='to-do-lists-page-v5'),
    path('create-to-do-list', views.ToDoListsView.as_view({'post': 'create'}), name='create-to-do-list-v5'),
    path(
        "delete-to-do-list/<int:list_id>",
        views.ToDoListsView.as_view({'delete': 'destroy'}),
        name="delete-to-do-list-v5",
    ),
    # path(
    #     "to-do-lists/<int:list_id>",
    #     views.TasksView.as_view(),
    #     name="tasks-page-v4",
    # ),
    # path("create-task/<int:list_id>", views.CreateTask.as_view(), name="create-task-v4"),

    # path(
    #     "create-task-with-uuid/<int:list_id>",
    #     views.CreateTaskWithUuidView.as_view(),
    #     name="create-task-with-uuid-v4",
    # ),
    # path(
    #     "delete-task/<int:task_id>/<int:list_id>",
    #     views.DeleteTaskView.as_view(),
    #     name="delete-task-v4",
    # ),
    # path(
    #     "create-uuid/<int:task_id>",
    #     views.CreateUuidView.as_view(),
    #     name="create-uuid-v4",
    # ),
    # path(
    #     "edit-task/<int:task_id>",
    #     views.EditTaskView.as_view(),
    #     name="edit-task-v4",
    # ),
]