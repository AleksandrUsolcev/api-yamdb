from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import User
from .permissions import AllowAdminOnly
from .serializers import (UserSignupSerializer, UserTokenSerializer,
                          UsersSerializer)
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response
from reviews.models import Category, Genre, Title

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer,TitlePostSerializer)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter)
    search_fields = ('name')
    lookup_field = 'slug'
    # permission_classes = (AdminOrReadOnly)


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter)
    search_fields = ('name')
    lookup_field = 'slug'
    # permission_classes = (AdminOrReadOnly)


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend)
    filterset_class = TitleFilter
    # permission_classes = (AdminOrReadOnly)


    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitlePostSerializer
        return TitleSerializer

class UserSignupViewSet(viewsets.ModelViewSet):
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data['username']
        code = request.data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if user.password != code:
            return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [AllowAdminOnly]
    pagination_class = LimitOffsetPagination
