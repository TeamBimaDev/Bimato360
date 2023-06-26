from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import permissions, viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.settings import api_settings

from .serializers import (
    UserSerializer,
    AuthTokenSerializer,
    ChangePasswordSerializer,
    ResetPasswordEmailRequestSerializer
)

from .models import User

from .signals import reset_password_signal


class CreateTokenView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='list-permissions')
    def list_permissions(self, request):
        permissions = Permission.objects.all()
        permissions_list = [{'id': perm.id, 'name': perm.name, 'codename': perm.codename} for perm in permissions]
        return Response(permissions_list)

    @action(detail=False, methods=['post'], url_path='manage-permissions')
    def manage_permissions(self, request):
        # Check if the user has the permission to access this endpoint
        if not request.user.has_perm('auth.change_permission'):
            return Response({'error': 'You do not have permission to manage permissions'},
                            status=status.HTTP_403_FORBIDDEN)

        new_permission_ids = set(request.data.get('permissions', []))
        current_permission_ids = set(request.user.user_permissions.values_list('id', flat=True))

        permissions_to_add = new_permission_ids - current_permission_ids
        permissions_to_remove = current_permission_ids - new_permission_ids

        with transaction.atomic():
            permissions_to_add = Permission.objects.filter(id__in=permissions_to_add)
            request.user.user_permissions.add(*permissions_to_add)

            permissions_to_remove = Permission.objects.filter(id__in=permissions_to_remove)
            request.user.user_permissions.remove(*permissions_to_remove)

        return Response({'status': 'Permissions updated successfully'})


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = get_user_model()
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong password."}, status=400)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=200)

        return Response(serializer.errors, status=400)


class PasswordResetView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = get_user_model().objects.get(email=serializer.data.get('email'))
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = request.build_absolute_uri('/')
            reset_password_link = f'{current_site}reset-password/{uid}/{token}/'

            reset_password_signal.send(
                sender=self.__class__,
                email=user.email,
                reset_password_link=reset_password_link,
            )

            return Response({'success': 'We have sent you a link to reset your password'}, status=200)
        else:
            return Response(serializer.errors, status=400)
