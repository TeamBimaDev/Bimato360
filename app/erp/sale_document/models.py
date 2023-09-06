from datetime import datetime, timedelta

from common.enums.sale_document_enum import SaleDocumentTypes
from common.enums.sale_document_enum import (
    get_sale_document_status,
    get_sale_document_types,
    get_sale_document_validity,
    get_sale_document_recurring_interval,
    get_sale_document_recurring_custom_unit,
    get_sale_document_recurring_cycle,
    SaleDocumentRecurringInterval,
    SaleDocumentRecurringCycle,
    get_payment_status,
)
from common.enums.transaction_enum import PaymentTermType
from core.abstract.models import AbstractModel
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import DecimalField, Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from erp.partner.models import BimaErpPartner
from erp.product.models import BimaErpProduct
from rest_framework.exceptions import ValidationError
from simple_history.models import HistoricalRecords
from treasury.payment_term.models import BimaTreasuryPaymentTerm
from treasury.transaction.models import BimaTreasuryTransaction
from treasury.transaction.models import TransactionSaleDocumentPayment


class BimaErpSaleDocumentProduct(models.Model):
    sale_document = models.ForeignKey("BimaErpSaleDocument", on_delete=models.PROTECT)
    product = models.ForeignKey("BimaErpProduct", on_delete=models.PROTECT)
    sale_document_public_id = models.UUIDField(blank=True, null=True, editable=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    reference = models.CharField(max_length=255, blank=False, null=False)
    quantity = models.DecimalField(
        max_digits=18, decimal_places=3, blank=False, null=False
    )
    unit_of_measure = models.CharField(
        max_length=255, blank=False, null=False, default="default"
    )
    unit_price = models.DecimalField(
        max_digits=18, decimal_places=3, blank=False, null=False
    )
    vat = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    vat_amount = models.DecimalField(
        max_digits=18, decimal_places=3, blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    discount_amount = models.DecimalField(
        max_digits=18, decimal_places=3, blank=True, null=True
    )
    total_without_vat = models.DecimalField(
        max_digits=18, decimal_places=3, blank=True, null=True
    )
    total_after_discount = models.DecimalField(
        max_digits=18, decimal_places=3, blank=True, null=True
    )
    total_price = models.DecimalField(
        max_digits=18, decimal_places=3, blank=True, null=True
    )
    history = HistoricalRecords()

    class Meta:
        unique_together = ("sale_document", "product")
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
        if (
                product.type == "STOCKABLE_PRODUCT"
                and product.quantity < quantity_to_add_sale_document
        ):
            return False
        return True


class BimaErpSaleDocument(AbstractModel):
    skip_child_validation_form_transaction = False
    number = models.CharField(
        max_length=32, null=False, blank=False, unique=True, verbose_name=_("Number")
    )
    date = models.DateField(null=False, blank=False, verbose_name=_("Date"))
    status = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        default="DRAFT",
        choices=get_sale_document_status(),
        verbose_name=_("Status"),
    )
    type = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        default="Quote",
        choices=get_sale_document_types(),
        verbose_name=_("Type"),
    )

    partner = models.ForeignKey(
        BimaErpPartner, on_delete=models.PROTECT, verbose_name=_("Partner")
    )
    vat_label = models.CharField(
        max_length=128, blank=True, null=True, default="", verbose_name=_("VAT Label")
    )
    vat_amount = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        blank=True,
        null=True,
        default=0,
        verbose_name=_("VAT Amount"),
    )
    note = models.TextField(blank=True, null=True, verbose_name=_("Note"))
    private_note = models.TextField(
        blank=True, null=True, verbose_name=_("Private Note")
    )
    validity = models.CharField(
        blank=True,
        null=True,
        choices=get_sale_document_validity(),
        verbose_name=_("Validity"),
    )
    payment_terms = models.ForeignKey(
        BimaTreasuryPaymentTerm,
        blank=True,
        null=True,
        verbose_name=_("Payment Terms"),
        on_delete=models.PROTECT,
        default=None,
    )
    delivery_terms = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("Delivery Terms")
    )
    total_amount_without_vat = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        blank=True,
        null=True,
        default=0,
        verbose_name=_("Total Amount without VAT"),
    )
    total_after_discount = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        blank=True,
        null=True,
        default=0,
        verbose_name=_("Total After Discount"),
    )
    total_vat = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        blank=True,
        null=True,
        default=0,
        verbose_name=_("Total VAT"),
    )
    total_amount = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        blank=True,
        null=True,
        default=0,
        verbose_name=_("Total Amount"),
    )
    total_discount = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        blank=True,
        null=True,
        default=0,
        verbose_name=_("Total Discount"),
    )
    parents = models.ManyToManyField(
        "self", symmetrical=False, blank=True, verbose_name=_("Parents")
    )
    is_recurring = models.BooleanField(
        default=False, blank=True, null=True, verbose_name=_("Is Recurring?")
    )
    is_recurring_parent = models.BooleanField(
        default=False, blank=True, null=True, verbose_name=_("Is Recurring Parent?")
    )
    is_recurring_ended = models.BooleanField(
        default=False, blank=True, null=True, verbose_name=_("Is Recurring Ended?")
    )
    recurring_initial_parent_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        default=None,
        verbose_name=_("Recurring Initial Parent ID"),
    )
    recurring_initial_parent_public_id = models.UUIDField(
        blank=True,
        null=True,
        default=None,
        verbose_name=_("Recurring Initial Parent Public ID"),
    )
    recurring_interval = models.CharField(
        blank=True,
        null=True,
        choices=get_sale_document_recurring_interval(),
        help_text="Interval for recurring sale documents",
        verbose_name=_("Recurring Interval"),
    )
    recurring_interval_type_custom_number = models.PositiveIntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name=_("Recurring Interval Type Custom Number"),
    )
    recurring_interval_type_custom_unit = models.CharField(
        blank=True,
        null=True,
        choices=get_sale_document_recurring_custom_unit(),
        verbose_name=_("Recurring Interval Type Custom Unit"),
    )
    recurring_cycle = models.CharField(
        blank=True,
        null=True,
        choices=get_sale_document_recurring_cycle(),
        verbose_name=_("Recurring Cycle"),
    )
    recurring_cycle_number_to_repeat = models.PositiveIntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name=_("Recurring Cycle Number to Repeat"),
    )
    recurring_cycle_stop_at = models.DateField(
        null=True, blank=True, verbose_name=_("Recurring Cycle Stop At")
    )
    recurring_cycle_stopped_at = models.DateField(
        null=True, blank=True, verbose_name=_("Recurring Cycle Stopped At")
    )
    recurring_last_generated_day = models.DateField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Recurring Last Generated Day"),
    )
    recurring_next_generated_day = models.DateField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Recurring Next Generated Day"),
    )
    recurring_reason_stop = models.TextField(
        null=True, blank=True, default=None, verbose_name=_("Recurring Reason Stop")
    )
    recurring_stopped_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="stopped_by",
        verbose_name=_("Recurring Stopped By"),
    )
    recurring_reason_reactivated = models.TextField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Recurring Reason Reactivated"),
    )
    recurring_reactivated_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reactivated_by",
        verbose_name=_("Recurring Reactivated By"),
    )
    recurring_reactivated_date = models.DateField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Recurring Reactivated Date"),
    )

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

    history = HistoricalRecords()
    sale_document_products = models.ManyToManyField(
        BimaErpProduct,
        through=BimaErpSaleDocumentProduct,
        verbose_name=_("Sale Document Products"),
    )
    transactions = models.ManyToManyField(
        BimaTreasuryTransaction,
        through=TransactionSaleDocumentPayment,
        related_name='sale_documents',
    )

    class Meta:
        ordering = ["-created"]
        permissions = []
        default_permissions = ()

    def save(self, *args, **kwargs):

        if self.pk is not None and not self.skip_child_validation_form_transaction:
            if self.bimaerpsaledocument_set.exists() and not self.is_recurring:
                raise ValidationError("Cannot modify a SaleDocument that has children.")
        self.validate_all_required_field_for_recurring()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.has_payment():
            raise ValidationError(_("Cannot delete this invoice, you need to unpaid it first!"))
        super(BimaErpSaleDocument, self).delete(*args, **kwargs)

    TYPE_DISPLAY_MAPPING = {
        SaleDocumentTypes.QUOTE.name: _("Quote"),
        SaleDocumentTypes.ORDER.name: _("Order"),
        SaleDocumentTypes.INVOICE.name: _("Invoice"),
        SaleDocumentTypes.CREDIT_NOTE.name: _("Credit note"),
    }

    @property
    def display_type(self):
        return self.TYPE_DISPLAY_MAPPING.get(self.type, self.type)

    @property
    def remain_amount(self):
        return self.total_amount - self.amount_paid

    def validate_all_required_field_for_recurring(self):
        if self.is_recurring:
            self.validate_custom_recurring_interval()
            self.validate_recurring_cycle_end_at()
            self.validate_recurring_cycle_end_after()

    def validate_custom_recurring_interval(self):
        if self.recurring_interval == SaleDocumentRecurringInterval.CUSTOM.name and (
                not self.recurring_interval_type_custom_number
                or not self.recurring_interval_type_custom_unit
        ):
            raise ValidationError(
                {"Error": _("CHOISIR_RECURRENT_CUSTOM_TYPE_UNIT_OR_NUMBER")}
            )

    def validate_recurring_cycle_end_at(self):
        if (
                self.recurring_cycle == SaleDocumentRecurringCycle.END_AT.name
                and not self.recurring_cycle_stop_at
        ):
            raise ValidationError({"Error": _("CHOISIR_RECURRENT_CYCLE_DATE_FIN")})
        if (
                self.recurring_cycle_stop_at
                and not self.is_recurring_ended
                and not self.pk
                and self.recurring_cycle_stop_at < datetime.now().date()
        ):
            raise ValidationError(
                {"Error": _("CHOISIR_RECURRENT_CYCLE_DATE_FIN_FUTURE")}
            )

    def validate_recurring_cycle_end_after(self):
        if (
                self.recurring_cycle == SaleDocumentRecurringCycle.END_AFTER.name
                and not self.recurring_cycle_number_to_repeat
        ):
            raise ValidationError({"Error": _("CHOISIR_RECURRENT_CYCLE_NOMBRE_CYCLE")})

    def calculate_payment_late(self):
        if self.payment_term.type != PaymentTermType.CUSTOM.name:
            due_date = self._calculate_due_date(self.date, self.payment_term.type)
            next_schedule = None
        else:
            due_date = None
            next_schedule = self.payment_term.schedules.first()
        # TODO this is not correct we need to check this logic
        if next_schedule:
            for schedule in self.payment_term.schedules.all():
                if schedule.due_date <= timezone.now().date():
                    due_date = schedule.due_date
                else:
                    break

        if due_date:
            now = timezone.now().date()
            if now > due_date:
                self.is_payment_late = True
                self.days_in_late = (now - due_date).days
            else:
                self.is_payment_late = False
                self.days_in_late = 0
        else:
            self.is_payment_late = False
            self.days_in_late = 0

        self.next_due_date = due_date
        self.save()

    def _calculate_due_date(self, sale_date, payment_term_type):
        if payment_term_type == PaymentTermType.IMMEDIATE.name:
            return sale_date
        elif payment_term_type == PaymentTermType.AFTER_ONE_WEEK.name:
            return sale_date + timedelta(weeks=1)
        elif payment_term_type == PaymentTermType.AFTER_TWO_WEEK.name:
            return sale_date + timedelta(weeks=2)
        elif payment_term_type == PaymentTermType.END_OF_MONTH.name:
            next_month = sale_date.replace(day=1) + timedelta(days=32)
            return (next_month.replace(day=1) - timedelta(days=1)).date()
        elif payment_term_type == PaymentTermType.NEXT_MONTH.name:
            next_month = sale_date.replace(day=1) + timedelta(days=32)
            return next_month.replace(day=1).date()
        else:
            return None

    def _update_last_due_date(self):
        self.last_due_date = self.next_due_date
        self.save()

    def has_payment(self):
        return self.transactionsaledocumentpayment_set.exists()


def update_sale_document_totals(sale_document):
    sale_document_products = BimaErpSaleDocumentProduct.objects.filter(
        sale_document=sale_document
    )
    totals = sale_document_products.aggregate(
        total_discounts=Sum("discount_amount", output_field=DecimalField()),
        total_taxes=Sum("vat_amount", output_field=DecimalField()),
        total_amount=Sum("total_price", output_field=DecimalField()),
        total_amount_without_vat=Sum("total_without_vat", output_field=DecimalField()),
        total_after_discount=Sum("total_after_discount", output_field=DecimalField()),
    )
    sale_document.total_discount = (
        totals["total_discounts"] if totals["total_discounts"] else 0
    )
    sale_document.total_vat = totals["total_taxes"] if totals["total_taxes"] else 0
    sale_document.total_amount = totals["total_amount"] if totals["total_amount"] else 0
    sale_document.total_amount_without_vat = (
        totals["total_amount_without_vat"] if totals["total_amount_without_vat"] else 0
    )
    sale_document.total_after_discount = (
        totals["total_after_discount"] if totals["total_after_discount"] else 0
    )
    sale_document.save()
