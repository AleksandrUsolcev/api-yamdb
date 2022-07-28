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

    def save(self, *args, **kwargs):
        if self.is_superuser and not self.role:
            self.role = 'admin'
        super().save(*args, **kwargs)


class Category(models.Model):
    """ Категории """
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(verbose_name='Слаг категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """ Жанры """
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг жанра')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """ Произведения """
    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.PositiveSmallIntegerField(verbose_name='Год создания')
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        null=True,
        blank=True,
        related_name='genre',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category',
        verbose_name='Категория'
    )
    description = models.CharField(max_length=256, null=True, blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """ Отзывы """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    score = models.SmallIntegerField(
        validators=[
            MinValueValidator(1, 'Допустимы значения 1 и более'),
            MaxValueValidator(10, 'Допустимы значения 10 и менее'),
        ],
        verbose_name='Рейтинг',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='Unique_review',
            ),
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    """ Комментарии """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор коммента',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
