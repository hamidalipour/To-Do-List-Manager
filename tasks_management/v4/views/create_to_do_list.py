
from rest_framework import generics

from tasks_management.models import ToDoList
from tasks_management.v4.serializer import ToDoListSerializer


class CreateToDoListView(generics.CreateAPIView):
    serializer_class = ToDoListSerializer
    queryset = ToDoList.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


    # def post(self, request):
    #     data = JSONParser().parse(request)
    #     serializer = ToDoListSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors)
