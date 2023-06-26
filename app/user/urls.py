"""
URL mappings for the user API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user import views

from .views import UserViewSet

from .views import ChangePasswordView

app_name = 'user'

router = DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('token/', views.CreateTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='change_password'),
    path('', include(router.urls)),
]
