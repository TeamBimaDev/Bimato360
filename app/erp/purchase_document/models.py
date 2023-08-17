from common.enums.purchase_document_enum import PurchaseDocumentTypes
from common.enums.purchase_document_enum import get_purchase_document_status, \
    get_purchase_document_types, get_purchase_document_validity
from core.abstract.models import AbstractModel
from django.db import models
from django.db.models import DecimalField, Sum
from django.utils.translation import gettext_lazy as _
from erp.partner.models import BimaErpPartner
from erp.product.models import BimaErpProduct
from rest_framework.exceptions import ValidationError
from simple_history.models import HistoricalRecords


class BimaErpPurchaseDocumentProduct(models.Model):
    purchase_document = models.ForeignKey('BimaErpPurchaseDocument', on_delete=models.PROTECT)
    product = models.ForeignKey('BimaErpProduct', on_delete=models.PROTECT)
    purchase_document_public_id = models.UUIDField(blank=True, null=True, editable=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    reference = models.CharField(max_length=255, blank=False, null=False)
    quantity = models.DecimalField(max_digits=18, decimal_places=3, blank=False, null=False)
    unit_of_measure = models.CharField(max_length=255, blank=False, null=False, default='default')
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
        unique_together = ('purchase_document', 'product')
        default_permissions = ()

    def save(self, *args, **kwargs):
        if self.purchase_document_id and not self.purchase_document_public_id:
            self.purchase_document_public_id = self.purchase_document.public_id
        self.calculate_totals()
        super().save(*args, **kwargs)
        update_purchase_document_totals(self.purchase_document)
        self.purchase_document.save()

    def delete(self, *args, **kwargs):
        purchase_document = self.purchase_document
        super().delete(*args, **kwargs)
        update_purchase_document_totals(purchase_document)
        purchase_document.save()

    def calculate_totals(self):
        self.total_without_vat = self.quantity * self.unit_price
        self.discount_amount = self.total_without_vat * (self.discount or 0) / 100
        self.total_after_discount = self.total_without_vat - self.discount_amount
        self.vat_amount = self.total_after_discount * (self.vat or 0) / 100
        self.total_price = self.total_after_discount + self.vat_amount


class BimaErpPurchaseDocument(AbstractModel):
    number = models.CharField(max_length=32, null=False, blank=False, unique=True)
    number_at_partner = models.CharField(max_length=32, null=True, blank=True, unique=False)
    date = models.DateField(null=False, blank=False)
    status = models.CharField(max_length=128, null=False,
                              blank=False, default="DRAFT",
                              choices=get_purchase_document_status())
    type = models.CharField(max_length=128, null=False,
                            blank=False, default="Quote",
                            choices=get_purchase_document_types())

    partner = models.ForeignKey(BimaErpPartner, on_delete=models.PROTECT)
    vat_label = models.CharField(max_length=128, blank=True, null=True, default="")
    vat_amount = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True, default=0)
    note = models.TextField(blank=True, null=True)
    private_note = models.TextField(blank=True, null=True)
    validity = models.CharField(blank=True, null=True, choices=get_purchase_document_validity())
    payment_term = models.CharField(max_length=100, blank=True, null=True)
    delivery_terms = models.CharField(max_length=100, blank=True, null=True)
    total_amount_without_vat = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True, default=0)
    total_after_discount = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True, default=0)
    total_vat = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True, default=0)
    total_amount = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True, default=0)
    total_discount = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True, default=0)
    parents = models.ManyToManyField('self', symmetrical=False, blank=True)
    history = HistoricalRecords()
    purchase_document_products = models.ManyToManyField(BimaErpProduct, through=BimaErpPurchaseDocumentProduct)

    class Meta:
        ordering = ['-created']
        permissions = []
        default_permissions = ()

    def save(self, *args, **kwargs):
        if self.pk is not None:  # only do this for existing instances, not when creating new ones
            if self.bimaerppurchasedocument_set.exists():
                raise ValidationError("Cannot modify a PurchaseDocument that has children.")
        super().save(*args, **kwargs)

    TYPE_DISPLAY_MAPPING = {
        PurchaseDocumentTypes.QUOTE.name: _("Quote"),
        PurchaseDocumentTypes.ORDER.name: _("Order"),
        PurchaseDocumentTypes.INVOICE.name: _("Invoice"),
        PurchaseDocumentTypes.RFQ.name: _("Request for Quotation"),

    }

    @property
    def display_type(self):
        return self.TYPE_DISPLAY_MAPPING.get(self.type, self.type)


def update_purchase_document_totals(purchase_document):
    purchase_document_products = BimaErpPurchaseDocumentProduct.objects.filter(purchase_document=purchase_document)
    totals = purchase_document_products.aggregate(
        total_discounts=Sum('discount_amount', output_field=DecimalField()),
        total_taxes=Sum('vat_amount', output_field=DecimalField()),
        total_amount=Sum('total_price', output_field=DecimalField()),
        total_amount_without_vat=Sum('total_without_vat', output_field=DecimalField()),
        total_after_discount=Sum('total_after_discount', output_field=DecimalField()),

    )
    purchase_document.total_discount = totals['total_discounts'] if totals['total_discounts'] else 0
    purchase_document.total_vat = totals['total_taxes'] if totals['total_taxes'] else 0
    purchase_document.total_amount = totals['total_amount'] if totals['total_amount'] else 0
    purchase_document.total_amount_without_vat = totals['total_amount_without_vat'] \
        if totals['total_amount_without_vat'] else 0
    purchase_document.total_after_discount = totals['total_after_discount'] if totals['total_after_discount'] else 0
    purchase_document.save()
