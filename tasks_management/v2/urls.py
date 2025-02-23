from django.urls import path

from tasks_management.v2 import views as personal_to_do_list_view

urlpatterns = [
    path(
        "to-do-lists",
        personal_to_do_list_view.ToDoListsPageView.as_view(),
        name="to-do-lists-page-v2",
    ),
    path(
        "to-do-lists/<int:list_id>",
        personal_to_do_list_view.TasksPageView.as_view(),
        name="tasks-page-v2",
    ),
    path(
        "create-task-with-uuid/<int:list_id>",
        personal_to_do_list_view.TasksPageView.as_view(),
        name="create-task" "-with-uuid-v2",
    ),
    path(
        "delete-to-do-list/<int:list_id>",
        personal_to_do_list_view.DeleteToDoListView.as_view(),
        name="delete-to-do-list-v2",
    ),
    path(
        "create-to-do-list",
        personal_to_do_list_view.CreateToDoListView.as_view(),
        name="create-to-do-list-v2",
    ),
    path(
        "create-task/<int:list_id>",
        personal_to_do_list_view.CreateTaskView.as_view(),
        name="create-task-v2",
    ),
    path(
        "handle-task/<int:task_id>/<int:list_id>",
        personal_to_do_list_view.HandleTaskView.as_view(),
        name="handle" "-task-v2",
    ),
    path(
        "create-uuid/<int:task_id>/<int:list_id>",
        personal_to_do_list_view.HandleTaskView.as_view(),
        name="create" "-uuid-v2",
    ),
    path(
        "delete-task/<int:task_id>/<int:list_id>",
        personal_to_do_list_view.DeleteTaskView.as_view(),
        name="delete" "-task-v2",
    ),
    path(
        "edit-task/<int:task_id>/<int:list_id>",
        personal_to_do_list_view.EditTaskView.as_view(),
        name="edit-task-v2",
    ),
]
