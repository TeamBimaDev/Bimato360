
from core.abstract.models import AbstractModel
from django.contrib.auth.models import Permission
from django.db import models


class BimaUserRole(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    active = models.BooleanField(default=True)
    note = models.TextField(null=True, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return f"{self.name, self.id}"

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()

