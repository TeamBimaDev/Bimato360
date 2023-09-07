import logging
from datetime import timedelta
from decimal import Decimal

from common.enums.sale_document_enum import SaleDocumentTypes, SaleDocumentPaymentStatus, SaleDocumentStatus
from common.enums.transaction_enum import PaymentTermType
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from .models import BimaErpSaleDocument

logger = logging.getLogger(__name__)


def verify_sale_document_payment_status():
    sale_documents = BimaErpSaleDocument.objects.filter(
        status=SaleDocumentStatus.CONFIRMED.name,
        type=SaleDocumentTypes.INVOICE.name
    ).exclude(payment_status=SaleDocumentPaymentStatus.PAID.name)

    sale_document_to_return = []
    for sale_document in sale_documents:
        logger.info(f"start verification payment status sale document {sale_document.public_id}")
        print(f"start verification payment status sale document {sale_document.public_id}")
        try:

            if sale_document.payment_terms.type != PaymentTermType.CUSTOM.name:
                _calculate_payment_late_type_not_custom(sale_document)
            else:
                _calculate_payment_late_type_custom(sale_document)
            sale_document_to_return.append(
                {"sale_document_public_ud": sale_document.public_id, "next_due_date": sale_document.next_due_date})
            logger.info(f"sale document verification {sale_document.public_id} succeeded")
            print(f"sale document verification {sale_document.public_id} succeeded")
        except Exception as ex:
            logger.error(f"sale document verification {sale_document.public_id} faild {ex}")
            print(f"sale document verification {sale_document.public_id} faild {ex}")

    return sale_document_to_return


def _calculate_payment_late_type_custom(sale_document):
    due_date = None
    next_schedule = sale_document.payment_terms.payment_term_details.first()

    is_initial_phase = False
    percentage_to_pay = 0
    next_calculated_due_date = sale_document.date
    if next_schedule:
        for index, schedule in enumerate(sale_document.payment_terms.payment_term_details.all().order_by('id')):
            logger.info(f"sale document {sale_document.public_id} custom type payment  index {index} verification  ")
            print(f"sale document {sale_document.public_id} custom type payment  index {index} verification  ")
            percentage_to_pay += schedule.percentage
            if sale_document.next_due_date is None:
                due_date = _calculate_due_date(sale_document.date, schedule.value)
                sale_document.next_due_date = due_date
                is_initial_phase = True
                break
            else:
                now = timezone.now().date()
                next_calculated_due_date = _calculate_due_date(next_calculated_due_date, schedule.value)
                logger.info(
                    f"sale document {sale_document.public_id} custom type payment  index {index} verification : next_calculated_due_date{next_calculated_due_date}  ")
                print(
                    f"sale document {sale_document.public_id} custom type payment  index {index} verification : next_calculated_due_date{next_calculated_due_date}  ")
                if next_calculated_due_date > now:
                    break
        if not is_initial_phase:
            sale_document.next_due_date = next_calculated_due_date
            due_date = next_calculated_due_date

        if due_date:
            now = timezone.now().date()
            if now <= due_date:
                amount_paid = _calculate_sum_amount_paid(sale_document)
                percentage_to_pay_decimal = Decimal(str(percentage_to_pay))
                if amount_paid is None or amount_paid == 0 or amount_paid < (
                        percentage_to_pay_decimal / 100) * sale_document.total_amount:
                    sale_document.is_payment_late = True
                    sale_document.days_in_late = (now - due_date).days
                else:
                    sale_document.is_payment_late = False
                    sale_document.days_in_late = 0
            else:
                sale_document.is_payment_late = False
                sale_document.days_in_late = 0
        else:
            sale_document.is_payment_late = False
            sale_document.days_in_late = 0

        sale_document.skip_child_validation_form_transaction = True
        sale_document.save()
        sale_document.skip_child_validation_form_transaction = False


def _calculate_payment_late_type_not_custom(sale_document):
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


def _calculate_sum_amount_paid(sale_document):
    transactions = sale_document.transactionsaledocumentpayment_set.all()
    return sum(tr.amount_paid for tr in transactions)
