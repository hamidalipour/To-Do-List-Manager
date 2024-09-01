from rest_framework import generics

from tasks_management.models import ToDoList
from tasks_management.v4.serializers import ToDoListSerializer


class CreateToDoListView(generics.CreateAPIView):
    serializer_class = ToDoListSerializer
    queryset = ToDoList.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


