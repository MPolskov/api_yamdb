from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Category, Genre
from .serializers import CategorySerializer, GenreSerializer
from .permissions import IsAdministrator


class CategoryViewSet(GenericViewSet, mixins.ListModelMixin,
                      mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdministrator, )


class GenreViewSet(GenericViewSet, mixins.ListModelMixin,
                   mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdministrator | IsAuthenticatedOrReadOnly, )
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
