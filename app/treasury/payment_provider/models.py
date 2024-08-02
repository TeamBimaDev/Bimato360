<<<<<<< HEAD
from core.abstract.models import AbstractModel
from django.db import models


class BimaTreasuryPaymentProvider(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    active = models.BooleanField(default=True)
    credentials = models.JSONField(null=True, blank=True)
    supports_tokenization = models.BooleanField(null=True, default=False)
    supports_manual_capture = models.BooleanField(null=True, default=False)
    supports_refunds = models.BooleanField(null=True, default=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()
=======
from core.abstract.models import AbstractModel
from django.db import models


class BimaTreasuryPaymentProvider(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    active = models.BooleanField(default=True)
    credentials = models.JSONField(null=True, blank=True)
    supports_tokenization = models.BooleanField(null=True, default=False)
    supports_manual_capture = models.BooleanField(null=True, default=False)
    supports_refunds = models.BooleanField(null=True, default=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()
>>>>>>> origin/ma-branch
