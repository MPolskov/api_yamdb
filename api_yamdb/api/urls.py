from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)

urlpatterns = [
    path('v1/auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/', include(router.urls)),
]
