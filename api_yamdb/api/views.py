from django.core.mail import send_mail
from rest_framework import permissions
from rest_framework import viewsets
import uuid
from reviews.models import User
from .serializers import UserSignupSerializer


class UserSignupViewSet(viewsets.ModelViewSet):
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        email = serializer.data['email']
        username = serializer.data['username']
        code = uuid.uuid4()
        user = User.objects.create_user(
            username=username,
            email=email,
            confirmation_code=code
        )
        user.save()
        send_mail(
            'YaMDb - Успешная регистрация',
            f'Добро пожаловать {username}! Ваш код подтверждения: {code}',
            from_email='service@yamdb.com',
            recipient_list=[email],
            fail_silently=False,
        )
