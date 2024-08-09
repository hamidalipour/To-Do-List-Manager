"""
URL configuration for _base project.

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
from django.urls import path, include
from personal_to_do_list import views as personalToDoListView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('login/', personalToDoListView.login_page, name='login'),
    path('logout/', personalToDoListView.logout_page, name='logout'),
    path('home-page', personalToDoListView.home_page, name='home-page'),
    path('', include('personal_to_do_list.urls')),
]
