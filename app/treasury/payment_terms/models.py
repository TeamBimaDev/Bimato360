from django.db import models
from core.abstract.models import AbstractModel


class BimaTreasuryPaymentTerms(AbstractModel):
    name = models.CharField(max_length=128, blank=False)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()
