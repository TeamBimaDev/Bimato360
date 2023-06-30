from django.db import models
from core.abstract.models import AbstractModel
from treasury.transaction_payment_method.models import BimaTreasuryTransactionPaymentMethod


class BimaTreasuryTransactionPaymentMethodCardTransferDetail(AbstractModel):
    transaction_payment_method = models.ForeignKey(model=BimaTreasuryTransactionPaymentMethod, on_delete=models.PROTECT,
                                                   null=True, blank=True)
    card_type = models.CharField(max_length=128, blank=True, null=True)
    last_four_digits = models.CharField(max_length=4, blank=True, null=True)
    name_on_card = models.CharField(max_length=128, blank=True, null=True)
    expiry_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['id']
        permissions = []
