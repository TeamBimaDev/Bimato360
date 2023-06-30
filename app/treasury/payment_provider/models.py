from django.db import models
from core.abstract.models import AbstractModel


class BimaTreasuryPaymentProvider(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    active = models.BooleanField(default=True)
    credentials = models.JSONField(null=True, blank=True)
    supports_tokenization = models.BooleanField(null=True, default=False)
    supports_manual_capture = models.BooleanField(null=True, default=False)
    supports_refunds = models.BooleanField(null=True, default=False)

    class Meta:
        ordering = ['id']
        permissions = []
