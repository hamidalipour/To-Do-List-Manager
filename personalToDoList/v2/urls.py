from django.urls import path
from personalToDoList.v2 import views as personalToDoListView

urlpatterns = [
    path('to-do-lists', personalToDoListView.ToDoListsPageView.as_view(), name='to-do-lists-page-v2'),
    path('to-do-lists/<int:list_id>/', personalToDoListView.TasksPageView.as_view(), name='tasks-page-v2'),
    path('create-to-do-list/', personalToDoListView.CreateToDoListView.as_view(), name='create-to-do-list-v2'),
    path('create-task/<int:list_id>', personalToDoListView.CreateTaskView.as_view(), name="create-task-v2"),
    path('handle-task/<int:task_id>', personalToDoListView.HandleTaskView.as_view(), name='handle-task-v2'),
]