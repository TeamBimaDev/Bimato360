from django.db import models
from core.abstract.models import AbstractModel

BANK_OR_CASH_CHOICES = (
    (1, 'Bank'),
    (2, 'Cash'),
)


class BimaTreasuryPaymentMethod(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    bank_or_cash = models.PositiveIntegerField(choices=BANK_OR_CASH_CHOICES, null=False, blank=False)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()
