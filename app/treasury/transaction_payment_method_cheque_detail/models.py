from django.db import models

from core.abstract.models import AbstractModel
from treasury.transaction_payment_method.models import BimaTreasuryTransactionPaymentMethod


class BimaTreasuryTransactionPaymentMethodChequeDetail(AbstractModel):
    transaction_payment_method = models.ForeignKey(model=BimaTreasuryTransactionPaymentMethod, on_delete=models.PROTECT, null=True, blank=True)
    bank_name = models.CharField(max_length=128, blank=True, null=True)
    cheque_number = models.CharField(max_length=128, blank=True, null=True)
    issue_date = models.DateField(null=True, blank=True)
    account_number = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        ordering = ['id']
        permissions = []
