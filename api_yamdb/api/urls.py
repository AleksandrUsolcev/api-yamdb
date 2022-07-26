from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()

router.register('auth/signup', views.UserSignupViewSet, basename='signup')

urlpatterns = [
    path('v1/', include(router.urls)),
]
