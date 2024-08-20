from rest_framework import viewsets
from rest_framework.response import Response
from tasks_management.models import ToDoList
from tasks_management.v6.serializers import ToDoListSerializer


class ToDoListsView(viewsets.ModelViewSet):
    queryset = ToDoList.objects.all()
    serializer_class = ToDoListSerializer

    def create(self, request, *args, **kwargs):
        serializer = ToDoListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.error_messages)

    def destroy(self, request, *args, **kwargs):
        try:
            to_do_list = ToDoList.objects.get(id=kwargs['pk'])
            for task in to_do_list.task_set.all():
                task.to_do_lists.remove(to_do_list)
                if not task.to_do_lists.exists():
                    task.delete()
            to_do_list.delete()
            return Response("to do list was deleted")
        except ToDoList.DoesNotExist:
            return Response("Invalid id")
