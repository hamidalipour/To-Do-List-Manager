from rest_framework import generics
from rest_framework.response import Response

from tasks_management.models import ToDoList
from tasks_management.v4.serializers import ToDoListSerializer


class DeleteToDoListView(generics.RetrieveDestroyAPIView):
    serializer_class = ToDoListSerializer
    queryset = ToDoList.objects.all()

    def get_object(self):
        to_do_list = self.queryset.get(id=self.kwargs["list_id"])
        if to_do_list.user != self.request.user:
            return Response("it is not your to do list")
        return to_do_list

    def delete(self, request, *args, **kwargs):
        if not ToDoList.objects.filter(id=self.kwargs['list_id']).exists():
            return Response("Invalid id")
        to_do_list = self.queryset.get(id=self.kwargs["list_id"])
        if to_do_list.user != self.request.user:
            return Response("it is not your to do list")
        to_do_list.delete()
        return Response("to do list was deleted")
