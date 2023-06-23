from django.shortcuts import get_object_or_404

from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Title, Review, Comment
from .filters import TitleFilterSet
from .permissions import (
    IsAdministratorOrReadOnly,
    IsAuthorModeratorAdminOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleListSerializer,
    ReviewSerializer,
    CommentSerializer,
)


class CustomViewSet(GenericViewSet, mixins.ListModelMixin,
                    mixins.CreateModelMixin, mixins.DestroyModelMixin):

    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdministratorOrReadOnly, )


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.order_by('id')
    serializer_class = CategorySerializer


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.order_by('id')
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.order_by('id')
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilterSet
    permission_classes = (IsAdministratorOrReadOnly, )

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleListSerializer
        return TitleSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
