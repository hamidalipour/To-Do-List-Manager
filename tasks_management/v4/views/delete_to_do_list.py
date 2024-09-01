from rest_framework import generics
from rest_framework.response import Response

from tasks_management.models import ToDoList
from tasks_management.v4.serializers import ToDoListSerializer


class DeleteToDoListView(generics.RetrieveDestroyAPIView):
    def get_queryset(self):
        return ToDoList.objects.filter(user=self.request.user).distinct()
