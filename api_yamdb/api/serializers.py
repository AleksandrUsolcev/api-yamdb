from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Genre, Title, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )

    def validate_year(self, value):
        current_year = timezone.now().year
        if not 0 <= value <= current_year:
            raise serializers.ValidationError(
                'год создания: недопустимое значение'
            )
        return value


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    # rating = ???

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class AuthSignupSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        email = data['email']
        username = data['username']
        user_email = User.objects.filter(email=data['email'])
        user_username = User.objects.filter(username=data['username'])
        if user_username.exists():
            raise serializers.ValidationError(f'Пользователь с именем '
                                              f'{username} уже существует')
        elif user_email.exists():
            raise serializers.ValidationError(f'Пользовтель с почтой {email} '
                                              f'уже существует')
        elif username == 'me':
            raise serializers.ValidationError(f'Использовать {username} '
                                              f'в качестве имени пользователя '
                                              f'запрещено')
        return data


class AuthTokenSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
