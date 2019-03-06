from rest_framework import viewsets
from .models import Note, NotedModel
from .serializers import NoteSerializer, NotedModelSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NotedModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = NotedModel.objects.all()
    serializer_class = NotedModelSerializer
