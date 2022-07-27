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
