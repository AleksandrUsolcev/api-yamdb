from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from reviews.models import User
from .serializers import (UserSignupSerializer, UserTokenSerializer,
                          UsersSerializer)


class UserSignupViewSet(viewsets.ModelViewSet):
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        email = serializer.data['email']
        username = serializer.data['username']
        user = User.objects.create_user(
            username=username,
            email=email,
            is_active=False
        )
        user.save()
        send_mail(
            'YaMDb - Успешная регистрация',
            message=f'Добро пожаловать {username}! Ваш код подтверждения: '
                    f'{user.password}',
            from_email='service@yamdb.com',
            recipient_list=[email],
            fail_silently=False,
        )

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(request.data, status=status.HTTP_200_OK)


class UserTokenViewSet(viewsets.ModelViewSet):
    serializer_class = UserTokenSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data['username']
        code = request.data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if user.password != code:
            return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        # скоро тут будет токен
        token = 'soon'
        return Response({'token': token}, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
