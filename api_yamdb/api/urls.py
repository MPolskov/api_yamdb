from rest_framework import routers
from django.urls import path, include

from .views import CategoryViewSet, GenreViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
