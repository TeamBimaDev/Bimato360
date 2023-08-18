from company.models import BimaCompany
from core.abstract.models import AbstractModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class BimaTreasuryCash(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    active = models.BooleanField(default=True)
    company = models.ForeignKey(BimaCompany, on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=14, decimal_places=3, verbose_name=_("Balance"), default=0)
    note = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['id']
        permissions = []
        default_permissions = ()
