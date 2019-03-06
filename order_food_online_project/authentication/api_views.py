from rest_framework import generics
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated

class UserListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
