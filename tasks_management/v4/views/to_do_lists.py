from rest_framework import generics

from tasks_management.models import ToDoList
from tasks_management.v4.serializers import ToDoListSerializer


class ToDoListsView(generics.ListAPIView):
    serializer_class = ToDoListSerializer

    def get_queryset(self):
        return ToDoList.objects.filter(user=self.request.user)

