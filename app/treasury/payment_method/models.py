<<<<<<< HEAD
from common.enums.transaction_enum import get_transaction_type_income_outcome, get_transaction_type_for_cash_or_bank
from core.abstract.models import AbstractModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class BimaTreasuryPaymentMethod(AbstractModel):
    name = models.CharField(max_length=128, blank=False)
    active = models.BooleanField(default=True)
    note = models.TextField(blank=True, null=True, verbose_name=_("Description/Note"))
    code = models.CharField(max_length=128, unique=True, null=True, blank=True)
    is_system = models.BooleanField(default=False)
    income_outcome = models.CharField(max_length=32, blank=False, null=False,
                                      choices=get_transaction_type_income_outcome(),
                                      verbose_name=_('INCOME_OUTCOME'))
    cash_bank = models.CharField(max_length=32, blank=False, null=False,
                                 choices=get_transaction_type_for_cash_or_bank(),
                                 verbose_name=_('CASH_BANK'))

    def __str__(self):
        return f"{self.name}  ({self.income_outcome})"

    class Meta:
        ordering = ['-created']
        permissions = []
        default_permissions = ()
=======
from common.enums.transaction_enum import get_transaction_type_income_outcome, get_transaction_type_for_cash_or_bank
from core.abstract.models import AbstractModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class BimaTreasuryPaymentMethod(AbstractModel):
    name = models.CharField(max_length=128, blank=False)
    active = models.BooleanField(default=True)
    note = models.TextField(blank=True, null=True, verbose_name=_("Description/Note"))
    code = models.CharField(max_length=128, unique=True, null=True, blank=True)
    is_system = models.BooleanField(default=False)
    income_outcome = models.CharField(max_length=32, blank=False, null=False,
                                      choices=get_transaction_type_income_outcome(),
                                      verbose_name=_('INCOME_OUTCOME'))
    cash_bank = models.CharField(max_length=32, blank=False, null=False,
                                 choices=get_transaction_type_for_cash_or_bank(),
                                 verbose_name=_('CASH_BANK'))

    def __str__(self):
        return f"{self.name}  ({self.income_outcome})"

    class Meta:
        ordering = ['-created']
        permissions = []
        default_permissions = ()
>>>>>>> origin/ma-branch
