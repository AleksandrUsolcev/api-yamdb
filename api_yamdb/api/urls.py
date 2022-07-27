from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, GenreViewSet,
                    TitleViewSet, TitlePostViewSet)

v1 = routers.DefaultRouter()
v1.register('titles', TitleViewSet, basename='titles')
v1.register('categories', CategoryViewSet, basename='categories')
v1.register('genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('v1/', include(v1.urls)),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()

router.register('auth/signup', views.UserSignupViewSet, basename='user_signup')
router.register('auth/token', views.UserTokenViewSet, basename='user_token')
router.register('users', views.UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
]
