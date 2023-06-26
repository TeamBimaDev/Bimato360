"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.settings import api_settings
from .models import User
from rest_framework.response import Response
from rest_framework import generics
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)
from rest_framework.permissions import IsAuthenticated
from .serializers import ChangePasswordSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

class CreateTokenView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    # authentication_classes = [authentication.isA]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user

class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
