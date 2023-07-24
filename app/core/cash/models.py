from django.db import models

from core.abstract.models import AbstractModel


class BimaCoreCash(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']
        permissions = []
        default_permissions = ()
