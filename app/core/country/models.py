from django.db import models
from core.abstract.models import AbstractModel
from core.currency.models import BimaCoreCurrency
class BimaCoreCountry(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    code = models.CharField(max_length=256, blank=True, null=True)
    address_format = models.CharField(max_length=256, blank=True, null=True)
    address_view_id = models.PositiveIntegerField(blank=True, null=True)
    phone_code = models.PositiveIntegerField(null=True)
    name_position = models.CharField(max_length=64, blank=True, null=True)
    vat_label = models.CharField(max_length=64, blank=True, null=True)
    state_required = models.BooleanField(null=True)
    zip_required = models.BooleanField(null=True)
    currency = models.ForeignKey(BimaCoreCurrency, on_delete=models.PROTECT)


    def __str__(self):
        return f"{self.name ,self.currency, self.id}"

    class Meta:
        ordering = ['name']
        permissions = []
