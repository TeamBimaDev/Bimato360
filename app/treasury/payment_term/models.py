from common.enums.transaction_enum import PaymentTermDetailType
from core.abstract.models import AbstractModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class BimaTreasuryPaymentTerm(AbstractModel):
    name = models.CharField(max_length=128, blank=False)
    active = models.BooleanField(default=True)
    note = models.TextField(blank=True, null=True, verbose_name=_("Description/Note"))
    code = models.CharField(max_length=128, unique=True, null=True, blank=True)
    is_system = models.BooleanField(default=False)

    def clean(self):
        lines = self.payment_term_details.all()
        if not lines:
            return

        total_percentage = sum(line.value for line in lines if line.type == PaymentTermDetailType.PERCENT.name)
        if any(line.type == PaymentTermDetailType.PERCENT.name for line in lines) and total_percentage != 100:
            raise ValidationError(_("Total percentage of percentage-type lines must be 100%."))

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()
