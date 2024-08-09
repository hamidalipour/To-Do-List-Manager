from django.urls import path
from personal_to_do_list.v3 import views as personal_to_do_list_view

urlpatterns = [
    path('to-do-lists', personal_to_do_list_view.ToDoListsPageView.as_view(), name='to-do-lists-page-v3'),
    path('to-do-lists/<int:list_id>/', personal_to_do_list_view.TasksPageView.as_view(), name='tasks-page-v3'),
    path('create-task-with-uuid/<int:list_id>', personal_to_do_list_view.CreateTaskWithUUIDView.as_view(), name='create-task-with-uuid-v3'),
    path('create-to-do-list/', personal_to_do_list_view.CreateToDoListView.as_view(), name='create-to-do-list-v3'),
    path('create-task/<int:list_id>', personal_to_do_list_view.CreateTaskView.as_view(), name="create-task-v3"),
    path('handle-task/<int:task_id>', personal_to_do_list_view.HandleTaskView.as_view(), name='handle-task-v3'),
    path('create-uuid/<int:task_id>', personal_to_do_list_view.CreateUUIDView.as_view(), name='create-uuid-v3'),
]