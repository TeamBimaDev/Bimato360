from common.enums.transaction_enum import PaymentTermType, get_payment_term_custom_type, get_payment_term_type

from core.abstract.models import AbstractModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class BimaTreasuryPaymentTerm(AbstractModel):
    name = models.CharField(max_length=128, blank=False)
    active = models.BooleanField(default=True)
    type = models.CharField(max_length=64, choices=get_payment_term_type(), blank=False, null=False)
    note = models.TextField(blank=True, null=True, verbose_name=_("Description/Note"))
    code = models.CharField(max_length=128, unique=True, null=True, blank=True)
    is_system = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk:
            if self.type == self.CUSTOM and not self.payment_term_details.exists():
                raise ValidationError('Custom payment terms must have associated schedules.')
        super(BimaTreasuryPaymentTerm, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_system:
            raise ValidationError(_("Cannot delete system item"))
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()


class BimaTreasuryPaymentTermDetail(models.Model):
    payment_term = models.ForeignKey(BimaTreasuryPaymentTerm, on_delete=models.CASCADE,
                                     related_name='payment_term_details')
    percentage = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], blank=False,
                                             null=False)
    value = models.CharField(max_length=64, choices=get_payment_term_custom_type(), blank=False, null=False)

    def save(self, *args, **kwargs):
        if self.payment_term.type != PaymentTermType.CUSTOM.name:
            raise ValidationError('Only custom payment terms can have schedules.')
        super(BimaTreasuryPaymentTermDetail, self).save(*args, **kwargs)
