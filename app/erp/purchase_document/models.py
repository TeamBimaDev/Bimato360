from common.enums.purchase_document_enum import PurchaseDocumentStatus
from common.enums.purchase_document_enum import PurchaseDocumentTypes
from common.enums.purchase_document_enum import get_payment_status
from common.enums.purchase_document_enum import get_purchase_document_status, \
    get_purchase_document_types, get_purchase_document_validity
from common.enums.transaction_enum import PaymentTermType
from common.service.purchase_sale_service import SalePurchaseService
from core.abstract.models import AbstractModel
from django.db import models
from django.db.models import DecimalField, Sum
from django.utils.translation import gettext_lazy as _
from erp.partner.models import BimaErpPartner
from erp.product.models import BimaErpProduct
from rest_framework.exceptions import ValidationError
from simple_history.models import HistoricalRecords
from treasury.payment_term.models import BimaTreasuryPaymentTerm
from treasury.transaction.models import BimaTreasuryTransaction, TransactionPurchaseDocumentPayment


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
        update_purchase_document_totals(self.purchase_document, re_save=False)
        self.purchase_document.save()

    def delete(self, *args, **kwargs):
        purchase_document = self.purchase_document
        super().delete(*args, **kwargs)
        update_purchase_document_totals(purchase_document, re_save=False)
        purchase_document.save()

    def calculate_totals(self):
        self.total_without_vat = self.quantity * self.unit_price
        self.discount_amount = self.total_without_vat * (self.discount or 0) / 100
        self.total_after_discount = self.total_without_vat - self.discount_amount
        self.vat_amount = self.total_after_discount * (self.vat or 0) / 100
        self.total_price = self.total_after_discount + self.vat_amount


class BimaErpPurchaseDocument(AbstractModel):
    skip_child_validation_form_transaction = False
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
    payment_terms = models.ForeignKey(
        BimaTreasuryPaymentTerm,
        blank=True,
        null=True,
        verbose_name=_("Payment Terms"),
        on_delete=models.PROTECT,
        default=None,
    )
    delivery_terms = models.CharField(max_length=100, blank=True, null=True)
    total_amount_without_vat = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True, default=0)
    total_after_discount = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True, default=0)
    total_vat = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True, default=0)
    total_amount = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True, default=0)
    total_discount = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True, default=0)
    parents = models.ManyToManyField('self', symmetrical=False, blank=True)
    history = HistoricalRecords()
    purchase_document_products = models.ManyToManyField(BimaErpProduct, through=BimaErpPurchaseDocumentProduct)
    payment_status = models.CharField(
        default="NOT_PAID", blank=True, null=True, choices=get_payment_status()
    )
    amount_paid = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        blank=True,
        null=True,
        default=0,
        verbose_name=_("Amount Paid"),
    )
    next_due_date = models.DateField(
        null=True, blank=True, verbose_name=_("Next Due Date")
    )
    is_payment_late = models.BooleanField(
        default=False, verbose_name=_("Is Payment Late?")
    )
    days_in_late = models.PositiveIntegerField(
        default=0, verbose_name=_("Days in Late")
    )
    last_due_date = models.DateField(
        null=True, blank=True, verbose_name=_("Last Due Date")
    )
    transactions = models.ManyToManyField(
        BimaTreasuryTransaction,
        through=TransactionPurchaseDocumentPayment,
        related_name='purchase_documents',
    )

    class Meta:
        ordering = ['-date']
        permissions = []
        default_permissions = ()

    def save(self, *args, **kwargs):
        if self.pk is not None and not self.skip_child_validation_form_transaction:
            if self.bimaerppurchasedocument_set.exists():
                raise ValidationError("Cannot modify a PurchaseDocument that has children.")
        self.verify_and_calculate_next_due_date()
        update_purchase_document_totals(self, re_save=False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.has_payment():
            raise ValidationError(_("Cannot delete this invoice, you need to unpaid it first!"))
        super(BimaErpPurchaseDocument, self).delete(*args, **kwargs)

    TYPE_DISPLAY_MAPPING = {
        PurchaseDocumentTypes.QUOTE.name: _("Quote"),
        PurchaseDocumentTypes.ORDER.name: _("Order"),
        PurchaseDocumentTypes.INVOICE.name: _("Invoice"),
        PurchaseDocumentTypes.RFQ.name: _("Request for Quotation"),

    }

    @property
    def display_type(self):
        return self.TYPE_DISPLAY_MAPPING.get(self.type, self.type)

    @property
    def remain_amount(self):
        return self.total_amount - self.amount_paid

    @property
    def translated_payment_status(self):
        return str(_(self.payment_status))

    def has_payment(self):
        return self.transactionpurchasedocumentpayment_set.exists()

    def verify_and_calculate_next_due_date(self):
        if (not self.pk or not self.status == PurchaseDocumentStatus.CONFIRMED.name or
                not self.type == PurchaseDocumentTypes.INVOICE.name or not self.payment_terms):
            self.is_payment_late = False
            self.days_in_late = 0
            self.next_due_date = None
        else:
            if self.payment_terms.type != PaymentTermType.CUSTOM.name:
                SalePurchaseService.calculate_payment_late_type_not_custom(self, re_save=False)
            else:
                SalePurchaseService.calculate_payment_late_type_custom(self, re_save=False)

    def calculate_sum_amount_paid(self, date_limit=None):
        if not self.pk or not self.transactionpurchasedocumentpayment_set:
            return 0
        transactions = self.transactionpurchasedocumentpayment_set.all()
        if not transactions:
            return 0

        if date_limit is not None:
            transactions = transactions.filter(transaction__date__lte=date_limit)
        return sum(tr.amount_paid for tr in transactions)


def update_purchase_document_totals(purchase_document, re_save=True):
    purchase_document_products = BimaErpPurchaseDocumentProduct.objects.filter(purchase_document=purchase_document)
    if not purchase_document_products:
        return
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
    if re_save:
        purchase_document.save()
