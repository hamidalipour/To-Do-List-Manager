from django.urls import path, include
urlpatterns = [
    path('v1/', include('personalToDoList.v1.urls')),
    path('v2/', include('personalToDoList.v2.urls')),
    path('v3/', include('personalToDoList.v3.urls')),
]