import logging
from datetime import timedelta
from decimal import Decimal

from common.enums.purchase_document_enum import PurchaseDocumentTypes, PurchaseDocumentPaymentStatus, \
    PurchaseDocumentStatus
from common.enums.transaction_enum import PaymentTermType
from dateutil.relativedelta import relativedelta
from django.apps import apps
from django.utils import timezone

logger = logging.getLogger(__name__)


def verify_purchase_document_payment_status():
    BimaErpPurchaseDocument = apps.get_model('erp', 'BimaErpPurchaseDocument')
    purchase_documents = BimaErpPurchaseDocument.objects.filter(
        status=PurchaseDocumentStatus.CONFIRMED.name,
        type=PurchaseDocumentTypes.INVOICE.name
    ).exclude(payment_status=PurchaseDocumentPaymentStatus.PAID.name)

    purchase_document_to_return = []
    for purchase_document in purchase_documents:
        if not purchase_document.payment_terms:
            continue
        try:
            logger.info(f"start verification payment status purchase document {purchase_document.public_id}")
            print(f"start verification payment status purchase document {purchase_document.public_id}")
            if purchase_document.payment_terms.type != PaymentTermType.CUSTOM.name:
                calculate_payment_late_type_not_custom(purchase_document)
            else:
                calculate_payment_late_type_custom(purchase_document)
            purchase_document_to_return.append(
                {"purchase_document_public_ud": purchase_document.public_id,
                 "next_due_date": purchase_document.next_due_date})
            logger.info(f"purchase document verification {purchase_document.public_id} succeeded")
            print(f"purchase document verification {purchase_document.public_id} succeeded")
        except Exception as ex:
            logger.error(f"purchase document verification {purchase_document.public_id} faild {ex}")
            print(f"purchase document verification {purchase_document.public_id} faild {ex}")

    return purchase_document_to_return


def calculate_payment_late_type_custom(purchase_document, re_save=True):
    current_date = timezone.now().date()
    due_dates = []
    payment_schedule = purchase_document.payment_terms.payment_term_details.all().order_by('id')

    next_due_date = purchase_document.date

    for schedule in payment_schedule:
        next_due_date = _calculate_due_date(next_due_date, schedule.value)
        due_dates.append({next_due_date: schedule.percentage})
        if next_due_date > current_date:
            break

    purchase_document.next_due_date = next_due_date

    percentage_to_pay = 0
    is_payment_late = False
    for due_date_entry in due_dates:
        due_date, percentage = list(due_date_entry.items())[0]
        amount_paid = _calculate_sum_amount_paid(purchase_document)
        percentage_to_pay += percentage

        if amount_paid < (Decimal(percentage_to_pay) / 100) * purchase_document.total_amount:
            if current_date > due_date:
                days_in_late = abs((current_date - due_date).days)
                purchase_document.days_in_late = days_in_late
                is_payment_late = True if days_in_late > 0 else False
                purchase_document.is_payment_late = True if days_in_late > 0 else False
                break

    if not purchase_document.next_due_date or not is_payment_late:
        purchase_document.is_payment_late = False
        purchase_document.days_in_late = 0

    if re_save:
        purchase_document.skip_child_validation_form_transaction = True
        purchase_document.save()
        purchase_document.skip_child_validation_form_transaction = False


def calculate_payment_late_type_not_custom(purchase_document, re_save=True):
    due_date = _calculate_due_date(purchase_document.date, purchase_document.payment_terms.type)
    purchase_document.next_due_date = due_date
    now = timezone.now().date()

    if due_date and now > due_date:
        amount_pad = _calculate_sum_amount_paid(purchase_document)
        if amount_pad < purchase_document.total_amount:
            purchase_document.is_payment_late = True
            purchase_document.days_in_late = (now - due_date).days
        else:
            purchase_document.is_payment_late = False
            purchase_document.days_in_late = 0
    else:
        purchase_document.is_payment_late = False
        purchase_document.days_in_late = 0
    if re_save:
        purchase_document.skip_child_validation_form_transaction = True
        purchase_document.save()
        purchase_document.skip_child_validation_form_transaction = False


def _calculate_due_date(purchase_date, payment_term_type):
    if payment_term_type == PaymentTermType.IMMEDIATE.name:
        return purchase_date
    elif payment_term_type == PaymentTermType.AFTER_ONE_WEEK.name:
        return purchase_date + timedelta(weeks=1)
    elif payment_term_type == PaymentTermType.AFTER_TWO_WEEK.name:
        return purchase_date + timedelta(weeks=2)
    elif payment_term_type == PaymentTermType.END_OF_MONTH.name:
        next_month = purchase_date.replace(day=1) + relativedelta(day=31)
        return next_month
    elif payment_term_type == PaymentTermType.NEXT_MONTH.name:
        next_month = purchase_date + relativedelta(months=1)
        return next_month
    else:
        return None


def _calculate_sum_amount_paid(purchase_document, date_limit=None):
    if not purchase_document.pk or not purchase_document.transactionpurchasedocumentpayment_set:
        return 0

    transactions = purchase_document.transactionpurchasedocumentpayment_set.all()
    if date_limit is not None:
        transactions = transactions.filter(transaction__date__lte=date_limit)
    return sum(tr.amount_paid for tr in transactions)
