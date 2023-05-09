from django.db import models

from core.abstract.models import AbstractModel

from core.currency.models import BimaCoreCurrency


class BimaCompany(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    mobile = models.CharField(max_length=32, blank=True, null=True)
    fax = models.CharField(max_length=32, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    language = models.CharField(max_length=32, blank=True, null=True)
    currency = models.ForeignKey(BimaCoreCurrency, on_delete=models.PROTECT)
    timezone = models.TimeField()


    def __str__(self):
        return f"{self.name ,self.public_id}"

    class Meta:
        ordering = ['name']
        permissions = []