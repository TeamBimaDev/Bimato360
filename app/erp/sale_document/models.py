from django.db import models
from django.db.models import DecimalField, Sum
from simple_history.models import HistoricalRecords

from common.enums.sale_document_enum import get_sale_document_status, \
    get_sale_document_types, get_sale_document_validity

from erp.partner.models import BimaErpPartner
from erp.product.models import BimaErpProduct

from core.abstract.models import AbstractModel


class BimaErpSaleDocumentProduct(models.Model):
    sale_document = models.ForeignKey('BimaErpSaleDocument', on_delete=models.CASCADE)
    product = models.ForeignKey('BimaErpProduct', on_delete=models.CASCADE)
    sale_document_public_id = models.UUIDField(blank=True, null=True, editable=False)
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
    history = HistoricalRecords()

    class Meta:
        unique_together = ('sale_document', 'product')

    def save(self, *args, **kwargs):
        if self.sale_document_id and not self.sale_document_public_id:
            self.sale_document_public_id = self.sale_document.public_id
        self.calculate_totals()
        super().save(*args, **kwargs)
        update_sale_document_totals(self.sale_document)
        self.sale_document.save()

    def delete(self, *args, **kwargs):
        sale_document = self.sale_document
        super().delete(*args, **kwargs)
        update_sale_document_totals(sale_document)
        sale_document.save()

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
                            blank=False, default="Quote",
                            choices=get_sale_document_types())

    partner = models.ForeignKey(BimaErpPartner, on_delete=models.PROTECT)
    vat_label = models.CharField(max_length=128, blank=True, null=True, default="")
    vat_amount = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True, default=0)
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


def update_sale_document_totals(sale_document):
    sale_document_products = BimaErpSaleDocumentProduct.objects.filter(sale_document=sale_document)
    totals = sale_document_products.aggregate(
        total_discounts=Sum('discount_amount', output_field=DecimalField()),
        total_taxes=Sum('vat_amount', output_field=DecimalField()),
        total_amount=Sum('total_price', output_field=DecimalField())
    )
    sale_document.total_discount = totals['total_discounts'] if totals['total_discounts'] else 0
    sale_document.total_vat = totals['total_taxes'] if totals['total_taxes'] else 0
    sale_document.total_amount = totals['total_amount'] if totals['total_amount'] else 0
    sale_document.save()
