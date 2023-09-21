from core.abstract.models import AbstractModel
from django.db import models
from treasury.transaction.models import BimaTreasuryTransaction


class BimaTreasuryRefund(AbstractModel):
    transaction = models.ForeignKey(
        BimaTreasuryTransaction, on_delete=models.PROTECT, null=True, blank=True
    )
    amount = models.DecimalField(
        max_digits=18, decimal_places=3, blank=False, null=False, default=0
    )
    reason = models.TextField(null=True, blank=True)
    date = models.DateField(null=False, blank=False)

    class Meta:
        ordering = ["-date"]
        permissions = []
        default_permissions = ()
