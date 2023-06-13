from django.db import models
from simple_history.models import HistoricalRecords
from django.db.models.signals import post_save

from common.enums.sale_document_enum import get_sale_document_status, \
    get_sale_document_types, get_sale_document_validity

from erp.partner.models import BimaErpPartner
from erp.product.models import BimaErpProduct

from core.abstract.models import AbstractModel


class BimaErpSaleDocumentProduct(models.Model):
    sale_document = models.ForeignKey('BimaErpSaleDocument', on_delete=models.CASCADE)
    product = models.ForeignKey('BimaErpProduct', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    reference = models.CharField(max_length=255, blank=False, null=False)
    quantity = models.DecimalField(max_digits=18, decimal_places=3, blank=False, null=False)
    unit_price = models.DecimalField(max_digits=18, decimal_places=3, blank=False, null=False)
    vat = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    vat_amount = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    total_without_vat = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    total_after_discount = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    total_price = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)

    class Meta:
        unique_together = ('sale_document', 'product')

    def save(self, *args, **kwargs):
        self.calculate_totals()
        super().save(*args, **kwargs)
        post_save.send(self.__class__, instance=self)

    def calculate_totals(self):
        self.total_without_vat = self.quantity * self.unit_price
        self.discount_amount = self.total_without_vat * (self.discount or 0) / 100
        self.total_after_discount = self.total_without_vat - self.discount_amount
        self.vat_amount = self.total_after_discount * (self.vat or 0) / 100
        self.total_price = self.total_after_discount + self.vat_amount


class BimaErpSaleDocument(AbstractModel):
    number = models.CharField(max_length=32, null=False, blank=False, unique=True)
    date = models.DateField(null=False, blank=False)
    status = models.CharField(max_length=128, null=False,
                              blank=False, default="DRAFT",
                              choices=get_sale_document_status())
    type = models.CharField(max_length=128, null=False,
                            blank=False, default="DRAFT",
                            choices=get_sale_document_types())

    partner = models.ForeignKey(BimaErpPartner, on_delete=models.PROTECT)
    note = models.TextField(blank=True, null=True)
    private_note = models.TextField(blank=True, null=True)
    validity = models.CharField(blank=True, null=True, choices=get_sale_document_validity())
    payment_terms = models.CharField(max_length=100, blank=True, null=True)
    delivery_terms = models.CharField(max_length=100, blank=True, null=True)
    total_vat = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    total_discount = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    parents = models.ManyToManyField('self', blank=True)
    history = HistoricalRecords()
    sale_document_products = models.ManyToManyField(BimaErpProduct, through=BimaErpSaleDocumentProduct)
