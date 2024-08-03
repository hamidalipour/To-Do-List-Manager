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
    path('to-do-lists', personalToDoListView.to_do_lists_page, name='to-do-lists-page'),
    path('/to-do-lists/<int:list_id>/', personalToDoListView.tasks_page, name='tasks-page'),
    path('create-to-do-list/', personalToDoListView.create_to_do_list, name='create-to-do-list'),
]
