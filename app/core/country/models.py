from django.db import models
from core.abstract.models import AbstractModel
from core.currency.models import BimaCoreCurrency


class BimaCoreCountry(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    code = models.CharField(max_length=256, blank=True, null=True, unique=True)
    iso3 = models.CharField(max_length=256, blank=True, null=True, unique=True)
    iso2 = models.CharField(max_length=256, blank=True, null=True, unique=True)
    phone_code = models.CharField(blank=True, null=True)
    capital = models.CharField(blank=True, null=True)
    address_format = models.CharField(max_length=256, blank=True, null=True)
    vat_label = models.CharField(max_length=64, blank=True, null=True)
    zip_required = models.BooleanField(null=True)
    currency = models.ForeignKey(BimaCoreCurrency, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name, self.currency, self.id}"

    class Meta:
        ordering = ['-name']
        permissions = []
        default_permissions = ()
