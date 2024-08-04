"""
URL configuration for toDoList project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from personalToDoList import views as personalToDoListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', personalToDoListView.login_page, name='login'),
    path('v1/to-do-lists', personalToDoListView.to_do_lists_page, name='to-do-lists-page-v1'),
    path('v1/to-do-lists/<int:list_id>/', personalToDoListView.tasks_page, name='tasks-page-v1'),
    path('v1/create-to-do-list/', personalToDoListView.create_to_do_list, name='create-to-do-list-v1'),
    path('v1/create-tasks/<int:list_id>', personalToDoListView.create_task, name="create-task-v1"),
    path('v1/handle-task/<int:task_id>', personalToDoListView.handle_task, name='handle-task-v1'),

    path('v2/to-do-lists', personalToDoListView.ToDoListsPageView.as_view(), name='to-do-lists-page-v2'),
    path('v2/to-do-lists/<int:list_id>/', personalToDoListView.TasksPageView.as_view(), name='tasks-page-v2'),
    path('v2/create-to-do-list/', personalToDoListView.CreateToDoListView.as_view(), name='create-to-do-list-v2'),
    path('v2/create-tasks/<int:list_id>', personalToDoListView.CreateTaskView.as_view(), name="create-task-v2"),
    path('v2/handle-task/<int:task_id>', personalToDoListView.HandleTaskView.as_view(), name='handle-task-v2'),
]
