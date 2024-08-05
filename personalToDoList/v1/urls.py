from django.urls import path
from personalToDoList.v1 import views as personalToDoListView

urlpatterns = [
    path('to-do-lists', personalToDoListView.to_do_lists_page, name='to-do-lists-page-v1'),
    path('to-do-lists/<int:list_id>/', personalToDoListView.tasks_page, name='tasks-page-v1'),
    path('create-to-do-list/', personalToDoListView.create_to_do_list, name='create-to-do-list-v1'),
    path('create-task/<int:list_id>', personalToDoListView.create_task, name="create-task-v1"),
    path('handle-task/<int:task_id>', personalToDoListView.handle_task, name='handle-task-v1'),
]