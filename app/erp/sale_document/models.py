from common.enums.sale_document_enum import SaleDocumentTypes
from common.enums.sale_document_enum import get_sale_document_status, \
    get_sale_document_types, get_sale_document_validity, get_sale_document_recurring_interval, \
    get_sale_document_recurring_custom_unit, get_sale_document_recurring_cycle, SaleDocumentRecurringInterval, \
    SaleDocumentRecurringCycle
from core.abstract.models import AbstractModel
from django.db import models
from django.db.models import DecimalField, Sum
from django.utils.translation import gettext_lazy as _
from erp.partner.models import BimaErpPartner
from erp.product.models import BimaErpProduct
from rest_framework.exceptions import ValidationError
from simple_history.models import HistoricalRecords


class BimaErpSaleDocumentProduct(models.Model):
    sale_document = models.ForeignKey('BimaErpSaleDocument', on_delete=models.PROTECT)
    product = models.ForeignKey('BimaErpProduct', on_delete=models.PROTECT)
    sale_document_public_id = models.UUIDField(blank=True, null=True, editable=False)
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
        unique_together = ('sale_document', 'product')
        default_permissions = ()

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

    @staticmethod
    def is_quantity_available(product, quantity_to_add_sale_document):
        if product.type == 'STOCKABLE_PRODUCT' and product.quantity < quantity_to_add_sale_document:
            return False
        return True


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
    total_amount_without_vat = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True, default=0)
    total_after_discount = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True, default=0)
    total_vat = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True, default=0)
    total_amount = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True, default=0)
    total_discount = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True, default=0)
    parents = models.ManyToManyField('self', symmetrical=False, blank=True)
    is_recurring = models.BooleanField(default=False, blank=True, null=True)
    recurring_initial_parent_id = models.PositiveIntegerField(blank=True, null=True)
    recurring_initial_parent_public_id = models.UUIDField(blank=True, null=True)
    recurring_interval = models.CharField(
        blank=True,
        null=True,
        choices=get_sale_document_recurring_interval(),
        help_text="Interval for recurring sale documents"
    )
    recurring_interval_type_custom_number = models.PositiveIntegerField(blank=True, null=True, default=0)
    recurring_interval_type_custom_unit = models.CharField(blank=True, null=True,
                                                           choices=get_sale_document_recurring_custom_unit())
    recurring_cycle = models.CharField(blank=True, null=True, choices=get_sale_document_recurring_cycle())
    recurring_cycle_number_to_repeat = models.PositiveIntegerField(blank=True, null=True, default=0)
    recurring_cycle_stop_at = models.DateField(null=True, blank=True)
    recurring_cycle_stopped_at = models.DateField(null=True, blank=True)
    history = HistoricalRecords()
    sale_document_products = models.ManyToManyField(BimaErpProduct, through=BimaErpSaleDocumentProduct)

    class Meta:
        ordering = ['-created']
        permissions = []
        default_permissions = ()

    def save(self, *args, **kwargs):
        if self.pk is not None:  # only do this for existing instances, not when creating new ones
            if self.bimaerpsaledocument_set.exists():
                raise ValidationError("Cannot modify a SaleDocument that has children.")
        self.validate_all_required_field_for_recurring()
        super().save(*args, **kwargs)

    TYPE_DISPLAY_MAPPING = {
        SaleDocumentTypes.QUOTE.name: _("Quote"),
        SaleDocumentTypes.ORDER.name: _("Order"),
        SaleDocumentTypes.INVOICE.name: _("Invoice"),
        SaleDocumentTypes.CREDIT_NOTE.name: _("Credit note"),
    }

    @property
    def display_type(self):
        return self.TYPE_DISPLAY_MAPPING.get(self.type, self.type)

    def validate_all_required_field_for_recurring(self):
        if self.is_recurring:
            self.validate_custom_recurring_interval()
            self.validate_recurring_cycle_end_at()
            self.validate_recurring_cycle_end_after()

    def validate_custom_recurring_interval(self):
        if (self.recurring_interval == SaleDocumentRecurringInterval.CUSTOM.name and
                (not self.recurring_interval_type_custom_number or not self.recurring_interval_type_custom_unit)):
            raise ValidationError({'Error': _('CHOISIR_RECURRENT_CUSTOM_TYPE_UNIT_OR_NUMBER')})

    def validate_recurring_cycle_end_at(self):
        if self.recurring_cycle == SaleDocumentRecurringCycle.END_AT.name and not self.recurring_cycle_stop_at:
            raise ValidationError({'Error': _('CHOISIR_RECURRENT_CYCLE_DATE_FIN')})

    def validate_recurring_cycle_end_after(self):
        if self.recurring_cycle == SaleDocumentRecurringCycle.END_AFTER.name and not self.recurring_cycle_number_to_repeat:
            raise ValidationError({'Error': _('CHOISIR_RECURRENT_CYCLE_NOMBRE_CYCLE')})


def update_sale_document_totals(sale_document):
    sale_document_products = BimaErpSaleDocumentProduct.objects.filter(sale_document=sale_document)
    totals = sale_document_products.aggregate(
        total_discounts=Sum('discount_amount', output_field=DecimalField()),
        total_taxes=Sum('vat_amount', output_field=DecimalField()),
        total_amount=Sum('total_price', output_field=DecimalField()),
        total_amount_without_vat=Sum('total_without_vat', output_field=DecimalField()),
        total_after_discount=Sum('total_after_discount', output_field=DecimalField()),

    )
    sale_document.total_discount = totals['total_discounts'] if totals['total_discounts'] else 0
    sale_document.total_vat = totals['total_taxes'] if totals['total_taxes'] else 0
    sale_document.total_amount = totals['total_amount'] if totals['total_amount'] else 0
    sale_document.total_amount_without_vat = totals['total_amount_without_vat'] \
        if totals['total_amount_without_vat'] else 0
    sale_document.total_after_discount = totals['total_after_discount'] if totals['total_after_discount'] else 0
    sale_document.save()
