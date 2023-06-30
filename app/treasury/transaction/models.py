from django.db import models
from core.abstract.models import AbstractModel

from erp.partner.models import BimaErpPartner
from treasury.payment_method.models import BimaTreasuryPaymentMethod
from treasury.transaction_payment_method.models import BimaTreasuryTransactionPaymentMethod

from common.enums.transaction_enum import get_transaction_types


class BimaTreasuryTransaction(AbstractModel):
    name = models.CharField(max_length=128, blank=False)
    transaction_payment_method = models.ManyToManyField(BimaTreasuryPaymentMethod,
                                                        through=BimaTreasuryTransactionPaymentMethod)
    partner = models.ForeignKey(BimaErpPartner, related_name="transactions", on_delete=models.CASCADE,
                                null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=get_transaction_types(), default='income')
    amount = models.DecimalField(max_digits=18, decimal_places=3, blank=False, null=False, default=0)
    date = models.DateField(null=False, blank=False, auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    note = models.TextField(blank=False)

    class Meta:
        ordering = ['-date']
        permissions = []
