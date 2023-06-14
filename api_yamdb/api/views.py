from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Category, Genre, Title
from .permissions import IsAdministrator
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleListSerializer,
)


class CustomViewSet(GenericViewSet, mixins.ListModelMixin,
                    mixins.CreateModelMixin, mixins.DestroyModelMixin):

    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdministrator | IsAuthenticatedOrReadOnly, )


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdministrator | IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleListSerializer
        return TitleSerializer
