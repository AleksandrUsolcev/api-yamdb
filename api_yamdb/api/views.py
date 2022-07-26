from rest_framework import permissions
from rest_framework import viewsets

from reviews.models import User
from .serializers import UserSignupSerializer


class UserSignupViewSet(viewsets.ModelViewSet):
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        email = serializer.data['email']
        username = serializer.data['username']
        user = User.objects.create_user(username=username, email=email)
        user.save()
