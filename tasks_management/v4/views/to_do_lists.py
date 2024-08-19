from rest_framework import generics
from rest_framework.response import Response

from tasks_management.models import ToDoList
from tasks_management.v4.serializer import ToDoListSerializer


class ToDoListsView(generics.ListAPIView):
    serializer_class = ToDoListSerializer
    def get_queryset(self):
        return ToDoList.objects.filter(user=self.request.user)

    # def get(self, request):
    #     to_do_lists = ToDoList.objects.filter(user=request.user)
    #     serializer = ToDoListSerializer(to_do_lists, many=True)
    #     return Response(serializer.data)
