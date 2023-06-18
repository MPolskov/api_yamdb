from rest_framework import routers
from django.urls import path, include

from .views import CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet, basename='Title')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
