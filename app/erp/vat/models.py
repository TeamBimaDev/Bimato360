from django.db import models
from core.abstract.models import AbstractModel


class BimaErpVat(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    rate = models.FloatField(blank=False, unique=False)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        permissions = []
