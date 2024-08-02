

from core.abstract.models import AbstractModel
from django.db import models


class BimaCoreSource(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()


