from django.db import models
from core.abstract.models import AbstractModel
from treasury.payment_terms.models import BimaTreasuryPaymentTerms


class BimaTreasuryPaymentTermsDetails(AbstractModel):
    name = models.CharField(max_length=128, blank=False)
    value = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    payment_terms = models.ForeignKey(model=BimaTreasuryPaymentTerms, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['id']
        permissions = []
