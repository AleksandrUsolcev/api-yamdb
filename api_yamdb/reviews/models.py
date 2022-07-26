from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    roles = (
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Аутентифицированный пользователь')
    )
    role = models.CharField(
        'Роль',
        choices=roles,
        max_length=10
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        max_length=300
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        default=0,
        max_length=40
    )
    email_valid = models.BooleanField(
        'Email подтвержден',
        default=False
    )
