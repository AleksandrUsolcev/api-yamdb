from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

v1 = DefaultRouter()
v1.register('titles', views.TitleViewSet, basename='titles')
v1.register('categories', views.CategoryViewSet, basename='categories')
v1.register('genres', views.GenreViewSet, basename='genres')
v1.register('auth/signup', views.UserSignupViewSet, basename='user_signup')
v1.register('auth/token', views.UserTokenViewSet, basename='user_token')
v1.register('users', views.UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(v1.urls)),
]
