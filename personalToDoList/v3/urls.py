from django.urls import path
from personalToDoList.v3 import views as personalToDoListView

urlpatterns = [
    path('to-do-lists', personalToDoListView.ToDoListsPageView.as_view(), name='to-do-lists-page-v3'),
    path('to-do-lists/<int:list_id>/', personalToDoListView.TasksPageView.as_view(), name='tasks-page-v3'),
    path('create-task-with-uuid/<int:list_id>', personalToDoListView.CreateTaskWithUUIDView.as_view(), name='create-task-with-uuid-v3'),
    path('create-to-do-list/', personalToDoListView.CreateToDoListView.as_view(), name='create-to-do-list-v3'),
    path('create-task/<int:list_id>', personalToDoListView.CreateTaskView.as_view(), name="create-task-v3"),
]