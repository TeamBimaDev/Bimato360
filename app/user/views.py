from datetime import timedelta

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework import permissions, viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.settings import api_settings

from .serializers import (
    UserSerializer,
    AuthTokenSerializer,
    ChangePasswordSerializer,
    ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, AdminCreateUserSerializer
)

from .models import User

from .signals import reset_password_signal, user_activated_signal
from common.permissions.app_permission import IsAdminOrSelfUser, IsAdminUser, CanEditOtherPassword, UserHasAddPermission

from core.abstract.pagination import DefaultPagination

from core.models import GlobalPermission


class CreateTokenView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    ordering = ['-name']
    pagination_class = DefaultPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAdminOrSelfUser]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        elif self.action in ['list_permissions', 'manage_permissions']:
            permission_classes = [permissions.IsAdminUser & permissions.IsAuthenticated & UserHasAddPermission]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return User.objects.all()

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='list-permissions')
    def list_permissions(self, request):
        content_type = ContentType.objects.get_for_model(GlobalPermission)
        permissions = Permission.objects.filter(content_type=content_type)
        permissions_list = [{'id': perm.id, 'name': perm.name, 'codename': perm.codename} for perm in permissions]
        return Response(permissions_list)

    @action(detail=True, methods=['post'], url_path='manage-permissions')
    def manage_permissions(self, request, pk=None):

        user_to_update = self.get_object()

        if not request.user.has_perm('user.user.can_add_permission'):
            return Response({'error': 'You do not have permission to manage permissions'},
                            status=status.HTTP_403_FORBIDDEN)

        new_permission_ids = set(request.data.get('permissions', []))
        current_permission_ids = set(user_to_update.user_permissions.values_list('id', flat=True))

        permissions_to_add = new_permission_ids - current_permission_ids
        permissions_to_remove = current_permission_ids - new_permission_ids

        with transaction.atomic():
            try:
                permissions_to_add = Permission.objects.filter(id__in=permissions_to_add)
                user_to_update.user_permissions.add(*permissions_to_add)

                permissions_to_remove = Permission.objects.filter(id__in=permissions_to_remove)
                user_to_update.user_permissions.remove(*permissions_to_remove)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'Permissions updated successfully'})

    @action(detail=True, methods=['get'], url_path='list_user_permissions')
    def list_user_permissions(self, request, pk=None):
        user = get_object_or_404(User, public_id=pk)
        user_permissions = user.user_permissions.all()

        permissions_list = [
            {
                'permission_id': perm.id,
                'permission_name': perm.name,
                'permission_codename': perm.codename
            }
            for perm in user_permissions
        ]

        response_data = {
            'user_public_id': user.public_id,
            'user_name': user.name,
            'permissions': permissions_list
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def get_object(self):
        obj = User.objects. \
            get_object_by_public_id(self.kwargs['pk'])
        return obj

    @action(detail=False, methods=['post'], url_path='create_by_admin')
    def create_by_admin(self, request):
        serializer = AdminCreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserActivationView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, user_id):
        user = get_user_model().objects.get(public_id=user_id)
        if request.user.has_perm('user.user.can_activate_account'):
            user.is_approved = True
            user.approved_by = request.user
            user.approved_at = timezone.now()
            user.save()
            user_activated_signal.send(sender=self.__class__, user=user, admin=request.user)
            return Response({'status': 'User activated'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You do not have permission to activate users'}, status=status.HTTP_403_FORBIDDEN)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = get_user_model()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]

        return [CanEditOtherPassword()]

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
            reset_password_link = f'{current_site}/api/user/reset-password/{uid}/{token}/'

            user.reset_password_token = token
            user.reset_password_uid = uid
            user.reset_password_time = timezone.now()
            user.save()

            reset_password_signal.send(
                sender=self.__class__,
                email=user.email,
                reset_password_link=reset_password_link,
            )

            return Response({'success': 'We have sent you a link to reset your password'}, status=200)
        else:
            return Response(serializer.errors, status=400)


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)

            token_matches = user.reset_password_token == token
            token_not_expired = timezone.now() - user.reset_password_time <= timedelta(hours=24)

            if not token_matches or not token_not_expired:
                return Response({'error': 'Token is not valid or has expired'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
        user.set_password(serializer.validated_data.get('password'))
        user.save()
        return Response({'success': True, 'message': 'Password reset successful'}, status=status.HTTP_200_OK)


class CreateUserPasswordForFirstTime(APIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({"detail": "Password has been reset."})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
