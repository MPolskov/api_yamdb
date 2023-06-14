from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from reviews.models import Category
from .serializers import CategorySerializer
from .permissions import IsAdministrator


class CategoryViewSet(GenericViewSet, mixins.ListModelMixin,
                      mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdministrator, )
