from django.db import models
from core.abstract.models import AbstractModel

from core.bank.models import BimaCoreBank
from core.cash.models import BimaCoreCash

from treasury.payment_provider.models import BimaTreasuryPaymentProvider


class BimaTreasuryTransactionPaymentMethod(AbstractModel):
    transaction = models.ForeignKey('BimaTreasuryTransaction', on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.ForeignKey('BimaTreasuryPaymentMethod', on_delete=models.SET_NULL, null=True, blank=True)
    payment_provider = models.ForeignKey(BimaTreasuryPaymentProvider, on_delete=models.SET_NULL, null=True, blank=True)
    # bank = models.ForeignKey(BimaCoreBank, on_delete=models.SET_NULL, null=True, blank=True)
    # cash = models.ForeignKey(BimaCoreCash, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=18, decimal_places=3, blank=False, null=False, default=0)
    reference = models.CharField(max_length=128, blank=True, null=True)
    idempotency_token = models.CharField(max_length=256, blank=True, unique=True, null=True)
    is_captured = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-created']
        permissions = []
        default_permissions = ()
