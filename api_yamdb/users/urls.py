from rest_framework import routers
from django.urls import path, include


from users.views import UserSignUpView, TokenView, UserViewSet

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', UserSignUpView.as_view()),
    path('v1/auth/token/', TokenView.as_view()),
    path('v1/', include(router.urls)),
]
