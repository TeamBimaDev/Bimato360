from core.abstract.models import AbstractModel
from core.bank.models import BimaCoreBank
from core.currency.models import BimaCoreCurrency
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _


class BimaTreasuryBankAccount(AbstractModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"), blank=False, null=False)
    account_number = models.CharField(max_length=50, verbose_name=_("RIB"), blank=False, null=False)
    iban = models.CharField(max_length=34, null=True, blank=True, verbose_name=_("IBAN"))
    bank = models.ForeignKey(BimaCoreBank, on_delete=models.PROTECT, verbose_name=_("Bank"))
    currency = models.ForeignKey(BimaCoreCurrency, on_delete=models.PROTECT, verbose_name=_("Currency"))
    balance = models.DecimalField(max_digits=14, decimal_places=3, verbose_name=_("Balance"))
    account_holder_name = models.CharField(max_length=255, verbose_name=_("Account Holder Name"), blank=False,
                                           null=False)
    notes = models.TextField(null=True, blank=True, verbose_name=_("Notes"))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.name, self.public_id}"

    class Meta:
        ordering = ['id']
        permissions = []
        default_permissions = ()
