from common.enums.transaction_enum import get_transaction_type_income_outcome
from core.abstract.models import AbstractModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class BimaTreasuryTransactionType(AbstractModel):
    name = models.CharField(max_length=128, blank=False)
    active = models.BooleanField(default=True)
    note = models.TextField(blank=True, null=True, verbose_name=_("Description/Note"))
    code = models.CharField(max_length=128, unique=True, null=True, blank=True)
    is_system = models.BooleanField(default=False)
    income_outcome = models.CharField(max_length=32, blank=False, null=False,
                                      choices=get_transaction_type_income_outcome(),
                                      verbose_name=_('INCOME_OUTCOME'))

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()
