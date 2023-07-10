import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.http import Http404


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, created_by_admin=False, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError(_('User must have an email address.'))
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.created_by_admin = created_by_admin
        user.public_id = uuid.uuid4()
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.public_id = uuid.uuid4()
        user.is_staff = True
        user.is_superuser = True
        user.is_approved = True
        user.save(using=self._db)

        return user

    def get_object_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    public_id = models.UUIDField(db_index=True, unique=True,
                                 default=uuid.uuid4, editable=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    reset_password_token = models.CharField(max_length=255, null=True, blank=True)
    reset_password_uid = models.CharField(max_length=255, null=True, blank=True)
    reset_password_time = models.DateTimeField(null=True, blank=True)

    is_password_change_when_created = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()

    def has_perm(self, perm, obj=None):
        return self.user_permissions.filter(codename=perm).exists()
