from django.urls import path

from tasks_management.v1 import views as personal_to_do_list_view

urlpatterns = [
    path(
        "to-do-lists",
        personal_to_do_list_view.to_do_lists_page,
        name="to-do-lists-page-v1",
    ),
    path(
        "to-do-lists/<int:list_id>",
        personal_to_do_list_view.tasks_page,
        name="tasks-page-v1",
    ),
    path(
        "create-task-with-uuid/<int:list_id>",
        personal_to_do_list_view.tasks_page,
        name="create-task-with-uuid-v1",
    ),
    path(
        "delete-to-do-list/<int:list_id>",
        personal_to_do_list_view.delete_to_do_list,
        name="delete-to-do-list-v1",
    ),
    path(
        "create-to-do-list",
        personal_to_do_list_view.create_to_do_list,
        name="create-to-do-list-v1",
    ),
    path(
        "create-task/<int:list_id>",
        personal_to_do_list_view.create_task,
        name="create-task-v1",
    ),
    path(
        "handle-task/<int:task_id>/<int:list_id>",
        personal_to_do_list_view.handle_task,
        name="handle-task-v1",
    ),
    path(
        "create-uuid/<int:task_id>/<int:list_id>",
        personal_to_do_list_view.handle_task,
        name="create-uuid-v1",
    ),
    path(
        "delete-task/<int:task_id>/<int:list_id>",
        personal_to_do_list_view.delete_task,
        name="delete-task-v1",
    ),
    path(
        "edit-task/<int:task_id>/<int:list_id>",
        personal_to_do_list_view.edit_task,
        name="edit-task-v1",
    ),
]
