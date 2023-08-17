from common.enums.transaction_enum import get_payment_term_detail_types
from core.abstract.models import AbstractModel
from django.db import models
from django.utils.translation import gettext_lazy as _

from treasury.payment_term.models import BimaTreasuryPaymentTerm


class BimaTreasuryPaymentTermDetail(AbstractModel):
    name = models.CharField(max_length=128, blank=False)
    value = models.DecimalField(max_digits=5, decimal_places=3, blank=False, null=False)
    type = models.CharField(max_length=50, choices=get_payment_term_detail_types(), verbose_name=_("Type"))
    payment_term = models.ForeignKey(BimaTreasuryPaymentTerm, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name="payment_term_details")

    number_of_days = models.PositiveIntegerField(verbose_name=_("Number of Days"))
    day_of_month = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Day of the Month"))

    class Meta:
        verbose_name_plural = _("Payment Term Lines")
        ordering = ['name']
        permissions = []
        default_permissions = ()

    def __str__(self):
        return f"{self.type} {self.value} on {self.number_of_days} day(s)"
