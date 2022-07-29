from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(AbstractUser):
    """ Переопределенный пользователь """
    roles = (
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Аутентифицированный пользователь')
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=roles,
        max_length=10,
        default='user'
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        max_length=300
    )
