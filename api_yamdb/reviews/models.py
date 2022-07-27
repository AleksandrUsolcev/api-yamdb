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
        max_length=10,
        default='user'
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        max_length=300
    )

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)
