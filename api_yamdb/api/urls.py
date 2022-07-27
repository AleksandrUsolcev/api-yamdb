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
