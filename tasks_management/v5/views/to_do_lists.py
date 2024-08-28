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
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.error_messages)

    def destroy(self, request, list_id):
        #ToDo
        to_do_list = ToDoList.objects.get(id=list_id)
        # if to_do_list.user != self.request.user:
        #     return Response("to do list doesn't belong to you")
        for task in to_do_list.task_set.all():
            task.to_do_lists.remove(to_do_list)
            if not task.to_do_lists.exists():
                task.delete()
        to_do_list.delete()
        return Response("to do list was deleted")
