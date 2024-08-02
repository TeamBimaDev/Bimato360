

from core.abstract.models import AbstractModel
from django.db import models


class BimaCoreNotificationType(AbstractModel):
    name = models.CharField(max_length=128, blank=False, null=False)
    active = models.BooleanField(default=True)
    code = models.CharField(max_length=128, unique=True, null=True, blank=True)
    is_system = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()


