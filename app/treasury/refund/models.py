from django.db import models
from core.abstract.models import AbstractModel
from treasury.transaction.models import BimaTreasuryTransaction


class BimaTreasuryRefund(AbstractModel):
    transaction = models.ForeignKey(model=BimaTreasuryTransaction, on_delete=models.PROTECT, null=True, blank=True)
    amount = models.DecimalField(max_digits=18, decimal_places=3, blank=False, null=False, default=0)
    reason = models.TextField(null=True, blank=True)
    date = models.DateField(null=False, blank=False)

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()
