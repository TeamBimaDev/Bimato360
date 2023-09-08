import logging
from datetime import timedelta
from decimal import Decimal

from common.enums.purchase_document_enum import PurchaseDocumentTypes, PurchaseDocumentPaymentStatus, \
    PurchaseDocumentStatus
from common.enums.transaction_enum import PaymentTermType
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from .models import BimaErpPurchaseDocument

logger = logging.getLogger(__name__)


def verify_purchase_document_payment_status():
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
                _calculate_payment_late_type_not_custom(purchase_document)
            else:
                _calculate_payment_late_type_custom(purchase_document)
            purchase_document_to_return.append(
                {"purchase_document_public_ud": purchase_document.public_id,
                 "next_due_date": purchase_document.next_due_date})
            logger.info(f"purchase document verification {purchase_document.public_id} succeeded")
            print(f"purchase document verification {purchase_document.public_id} succeeded")
        except Exception as ex:
            logger.error(f"purchase document verification {purchase_document.public_id} faild {ex}")
            print(f"purchase document verification {purchase_document.public_id} faild {ex}")

    return purchase_document_to_return


def _calculate_payment_late_type_custom(purchase_document):
    due_date = None
    next_schedule = purchase_document.payment_terms.payment_term_details.first()

    is_initial_phase = False
    percentage_to_pay = 0
    next_calculated_due_date = purchase_document.date
    if next_schedule:
        for index, schedule in enumerate(purchase_document.payment_terms.payment_term_details.all().order_by('id')):
            logger.info(
                f"purchase document {purchase_document.public_id} custom type payment  index {index} verification  ")
            print(f"purchase document {purchase_document.public_id} custom type payment  index {index} verification  ")
            percentage_to_pay += schedule.percentage
            if purchase_document.next_due_date is None:
                due_date = _calculate_due_date(purchase_document.date, schedule.value)
                purchase_document.next_due_date = due_date
                is_initial_phase = True
                break
            else:
                now = timezone.now().date()
                next_calculated_due_date = _calculate_due_date(next_calculated_due_date, schedule.value)
                logger.info(
                    f"purchase document {purchase_document.public_id} custom type payment  index {index} verification : next_calculated_due_date{next_calculated_due_date}  ")
                print(
                    f"purchase document {purchase_document.public_id} custom type payment  index {index} verification : next_calculated_due_date{next_calculated_due_date}  ")
                if next_calculated_due_date > now:
                    break
        if not is_initial_phase:
            purchase_document.next_due_date = next_calculated_due_date
            due_date = next_calculated_due_date

        if due_date:
            now = timezone.now().date()
            if now > due_date:
                amount_paid = _calculate_sum_amount_paid(purchase_document)
                percentage_to_pay_decimal = Decimal(str(percentage_to_pay))
                if amount_paid is None or amount_paid == 0 or amount_paid < (
                        percentage_to_pay_decimal / 100) * purchase_document.total_amount:
                    purchase_document.is_payment_late = True
                    purchase_document.days_in_late = (now - due_date).days
                else:
                    purchase_document.is_payment_late = False
                    purchase_document.days_in_late = 0
            else:
                purchase_document.is_payment_late = False
                purchase_document.days_in_late = 0
        else:
            purchase_document.is_payment_late = False
            purchase_document.days_in_late = 0

        purchase_document.skip_child_validation_form_transaction = True
        purchase_document.save()
        purchase_document.skip_child_validation_form_transaction = False


def _calculate_payment_late_type_not_custom(purchase_document):
    due_date = _calculate_due_date(purchase_document.date, purchase_document.payment_terms.type)

    if due_date:
        now = timezone.now().date()
        if now > due_date:
            purchase_document.is_payment_late = True
            purchase_document.days_in_late = (now - due_date).days
        else:
            purchase_document.is_payment_late = False
            purchase_document.days_in_late = 0
    else:
        purchase_document.is_payment_late = False
        purchase_document.days_in_late = 0

    purchase_document.next_due_date = due_date
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


def _calculate_sum_amount_paid(purchase_document):
    transactions = purchase_document.transactionpurchasedocumentpayment_set.all()
    return sum(tr.amount_paid for tr in transactions)
