
from django.db import models

from core.abstract.models import AbstractModel


class BimaCoreCurrency(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    symbol = models.CharField(max_length=16, blank=True, null=True)
    rounding = models.PositiveIntegerField(blank=True, null=True)
    decimal_places = models.PositiveIntegerField(blank=True, null=True)
    active = models.BooleanField(null=True)
    position = models.CharField(max_length=64, blank=True, null=True)
    currency_unit_label = models.CharField(max_length=64, blank=True, null=True)
    currency_subunit_label = models.CharField(max_length=64, blank=True, null=True)



    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        permissions = []
