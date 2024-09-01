from rest_framework import viewsets
from rest_framework.response import Response

from tasks_management.models import ToDoList
from tasks_management.v5.serializers import ToDoListSerializer


class ToDoListsView(viewsets.ViewSet):
    def list(self, request):
        queryset = ToDoList.objects.filter(user=request.user)
        serializer = ToDoListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ToDoListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)

    def destroy(self, request, list_id):
        if not ToDoList.objects.filter(id=list_id, user=self.request.user).exists():
            return Response("invalid id")
        to_do_list = ToDoList.objects.get(id=list_id)
        to_do_list.delete()
        return Response("to do list was deleted")
