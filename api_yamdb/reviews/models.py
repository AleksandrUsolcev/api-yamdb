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

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(verbose_name='Слаг категории')

    class Meta:
        verbose_name = 'Категория'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг жанра')

    class Meta:
        verbose_name = 'Жанр'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.PositiveSmallIntegerField(verbose_name=' Год создания')
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='genre',
        verbose_name='Жанр')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 related_name='category',
                                 verbose_name='Категория')

    class Meta:
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name
