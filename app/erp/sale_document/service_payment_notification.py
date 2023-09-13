import logging
from datetime import timedelta
from decimal import Decimal

from common.enums.sale_document_enum import SaleDocumentTypes, SaleDocumentPaymentStatus, SaleDocumentStatus
from common.enums.transaction_enum import PaymentTermType
from dateutil.relativedelta import relativedelta
from django.apps import apps
from django.utils import timezone

logger = logging.getLogger(__name__)


def verify_sale_document_payment_status():
    BimaErpSaleDocument = apps.get_model('erp', 'BimaErpSaleDocument')
    sale_documents = BimaErpSaleDocument.objects.filter(
        status=SaleDocumentStatus.CONFIRMED.name,
        type=SaleDocumentTypes.INVOICE.name
    ).exclude(payment_status=SaleDocumentPaymentStatus.PAID.name)

    sale_document_to_return = []
    for sale_document in sale_documents:
        if not sale_document.payment_terms:
            continue
        try:
            logger.info(f"start verification payment status sale document {sale_document.public_id}")
            print(f"start verification payment status sale document {sale_document.public_id}")
            if sale_document.payment_terms.type != PaymentTermType.CUSTOM.name:
                calculate_payment_late_type_not_custom(sale_document)
            else:
                calculate_payment_late_type_custom(sale_document)
            sale_document_to_return.append(
                {"sale_document_public_ud": sale_document.public_id, "next_due_date": sale_document.next_due_date})
            logger.info(f"sale document verification {sale_document.public_id} succeeded")
            print(f"sale document verification {sale_document.public_id} succeeded")
        except Exception as ex:
            logger.error(f"sale document verification {sale_document.public_id} faild {ex}")
            print(f"sale document verification {sale_document.public_id} faild {ex}")

    return sale_document_to_return


def calculate_payment_late_type_custom(sale_document, re_save=True):
    current_date = timezone.now().date()
    due_dates = []
    payment_schedule = sale_document.payment_terms.payment_term_details.all().order_by('id')

    next_due_date = sale_document.date

    for schedule in payment_schedule:
        next_due_date = _calculate_due_date(next_due_date, schedule.value)
        due_dates.append({next_due_date: schedule.percentage})
        if next_due_date > current_date:
            break

    sale_document.next_due_date = next_due_date

    percentage_to_pay = 0
    is_payment_late = False
    for due_date_entry in due_dates:
        due_date, percentage = list(due_date_entry.items())[0]
        amount_paid = _calculate_sum_amount_paid(sale_document)
        percentage_to_pay += percentage

        if amount_paid < (Decimal(percentage_to_pay) / 100) * sale_document.total_amount:
            days_in_late = abs((current_date - due_date).days)
            sale_document.days_in_late = days_in_late
            is_payment_late = True if days_in_late > 0 else False
            sale_document.is_payment_late = True if days_in_late > 0 else False
            break

    if not sale_document.next_due_date or not is_payment_late:
        sale_document.is_payment_late = False
        sale_document.days_in_late = 0

    if re_save:
        sale_document.skip_child_validation_form_transaction = True
        sale_document.save()
        sale_document.skip_child_validation_form_transaction = False


def calculate_payment_late_type_not_custom(sale_document, re_save=True):
    due_date = _calculate_due_date(sale_document.date, sale_document.payment_terms.type)

    if due_date:
        now = timezone.now().date()
        if now > due_date:
            sale_document.is_payment_late = True
            sale_document.days_in_late = (now - due_date).days
        else:
            sale_document.is_payment_late = False
            sale_document.days_in_late = 0
    else:
        sale_document.is_payment_late = False
        sale_document.days_in_late = 0

    sale_document.next_due_date = due_date
    if re_save:
        sale_document.skip_child_validation_form_transaction = True
        sale_document.save()
        sale_document.skip_child_validation_form_transaction = False


def _calculate_due_date(sale_date, payment_term_type):
    if payment_term_type == PaymentTermType.IMMEDIATE.name:
        return sale_date
    elif payment_term_type == PaymentTermType.AFTER_ONE_WEEK.name:
        return sale_date + timedelta(weeks=1)
    elif payment_term_type == PaymentTermType.AFTER_TWO_WEEK.name:
        return sale_date + timedelta(weeks=2)
    elif payment_term_type == PaymentTermType.END_OF_MONTH.name:
        next_month = sale_date.replace(day=1) + relativedelta(day=31)
        return next_month
    elif payment_term_type == PaymentTermType.NEXT_MONTH.name:
        next_month = sale_date + relativedelta(months=1)
        return next_month
    else:
        return None


def _calculate_sum_amount_paid(sale_document, date_limit=None):
    transactions = sale_document.transactionsaledocumentpayment_set.all()
    if date_limit is not None:
        transactions = transactions.filter(transaction__date__lte=date_limit)
    return sum(tr.amount_paid for tr in transactions)
