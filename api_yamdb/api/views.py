from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, User
from .permissions import AllowAdminOnly, AllowAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, TitlePostSerializer,
                          AuthSignupSerializer, AuthTokenSerializer,
                          UsersSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AllowAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AllowAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    # filter_backends = (DjangoFilterBackend)
    # filterset_class = TitleFilter
    permission_classes = (AllowAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitlePostSerializer
        return TitleSerializer


class AuthSignupViewSet(viewsets.ModelViewSet):
    serializer_class = AuthSignupSerializer
    permission_classes = (AllowAny,)

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


class AuthTokenViewSet(viewsets.ModelViewSet):
    serializer_class = AuthTokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        username = request.data['username']
        code = request.data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if user.password != code:
            return Response('Неверный код', status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (AllowAdminOnly,)
    pagination_class = LimitOffsetPagination
