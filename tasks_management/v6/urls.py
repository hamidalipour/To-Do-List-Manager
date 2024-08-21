from django.urls import include, path
from rest_framework import routers

from tasks_management.v6 import views

router = routers.DefaultRouter()
router.register('to-do-lists', views.ToDoListsView, basename='to-do-lists-v6')
router.register('tasks', views.TasksView, basename='tasks-v6')
router.register('tokens', views.TokensView, basename='tokens-v6')
# router.register('to-do-lists/<int:pk>', views.ToDoListsView, basename='to-do-list-item-v6')
# router.register(r'create-to-do-list', views.CreateToDoListView, basename='create-to-do-list-v5')

urlpatterns = [
    path('', include(router.urls)),

]