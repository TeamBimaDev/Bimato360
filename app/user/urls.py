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

from user.views import CreateTokenView, UserPermissionViewSet, ListPermissionsViewSet

app_name = 'user'

router = DefaultRouter()
router.register(r'permissions', UserPermissionViewSet, basename='user-permission')
router.register(r'list-permissions', ListPermissionsViewSet, basename='list-permissions')

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('', include(router.urls)),
]
