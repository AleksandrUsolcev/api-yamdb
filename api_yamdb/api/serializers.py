from rest_framework import serializers

from reviews.models import User


class UserSignupSerializer(serializers.ModelSerializer):
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


class TokenSerializer(serializers.ModelSerializer):
    pass
