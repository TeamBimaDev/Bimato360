"""
URL mappings for the user API.
"""
from .views import PasswordResetView, PasswordResetConfirmView, UserActivationView, CreateUserPasswordForFirstTime
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
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
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('activate_user_account/<str:user_id>/', UserActivationView.as_view(), name='activate_user_account'),
    path('user_activate_and_change_password/<uidb64>/<token>/', CreateUserPasswordForFirstTime.as_view(),
         name='user_activate_and_change_password'),
    path('', include(router.urls)),
]
