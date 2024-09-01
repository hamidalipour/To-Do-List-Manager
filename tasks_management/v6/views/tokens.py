from rest_framework import viewsets

from tasks_management.models import Task, Token
from tasks_management.v6.serializers import NewTokenSerializer
from rest_framework.response import Response


class TokensView(viewsets.ModelViewSet):
    serializer_class = NewTokenSerializer

    def get_queryset(self):
        return Token.objects.filter(task__to_do_lists__user=self.request.user)
