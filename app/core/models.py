from django.db import models
from django.contrib.auth.models import Permission


class GlobalPermission(models.Model):
    """
    This model is used for the sole purpose of creating global permissions
    that are not associated with a specific model.
    """
    pass


class CustomPermission(models.Model):
    permission = models.OneToOneField(Permission, on_delete=models.CASCADE)
    gp_permission = models.CharField(max_length=255)
