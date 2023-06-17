from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from reviews.models import Category, Genre, Title
from .permissions import IsAdministratorOrReadOnly
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
    permission_classes = (IsAdministratorOrReadOnly, )


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    permission_classes = (IsAdministratorOrReadOnly, )

    def get_queryset(self):
        queryset = Title.objects.all().order_by('id')
        filterset_fields = ('name', 'year')
        filterset_slug_fields = ('genre', 'category')
        kwargs = {}

        for field in filterset_fields:
            value = self.request.query_params.get(field)
            if value:
                kwargs[field] = value

        for field in filterset_slug_fields:
            value = self.request.query_params.get(field)
            if value:
                kwargs[f'{field}__slug'] = value

        if kwargs:
            queryset = queryset.filter(**kwargs)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleListSerializer
        return TitleSerializer
