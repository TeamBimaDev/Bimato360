from django.db import models

from core.abstract.models import AbstractModel


class BimaErpUnitOfMeasure(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        permissions = []
