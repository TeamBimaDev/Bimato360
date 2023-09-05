import logging
import uuid

from common.enums.sale_document_enum import SaleDocumentPaymentStatus
from django.apps import apps
from django.db import transaction

logger = logging.getLogger(__name__)


def verify_transaction_public_ids(public_id):
    if len(public_id) > 0 and all(uuid.UUID(public_id, version=4) for public_id in public_id):
        return True
    return False


def handle_invoice_payment(sale_document, transaction_public_ids):
    if verify_transaction_public_ids(transaction_public_ids):
        try:
            delete_old_paid_transaction_sale_document(sale_document)
            update_amount_paid_document(sale_document, 0, SaleDocumentPaymentStatus.NOT_PAID.name)
            handle_invoice_payment_customer_invoice(sale_document, transaction_public_ids)
            handle_amount_paid_and_status_paid_sale_document(sale_document)
        except Exception as ex:
            logger.error(f"An error occurred while saving payment invoice: {ex}", exc_info=True,
                         extra={'object_id': object.id})


def delete_old_paid_transaction_sale_document(sale_document):
    with transaction.atomic():
        TransactionSaleDocumentPayment = apps.get_model('treasury', 'TransactionSaleDocumentPayment')
        old_transactions_payments = TransactionSaleDocumentPayment.objects.filter(sale_document=sale_document)
        old_transactions_payments.delete()


def handle_invoice_payment_customer_invoice(sale_document, transaction_public_ids):
    BimaTreasuryTransaction = apps.get_model('treasury', 'BimaTreasuryTransaction')
    TransactionSaleDocumentPayment = apps.get_model('treasury', 'TransactionSaleDocumentPayment')

    unpaid_amount = sale_document.total_amount - sale_document.amount_paid
    transactions = BimaTreasuryTransaction.objects.filter(
        public_id__in=transaction_public_ids
    ).order_by('date')

    for trans in transactions:
        update_remaining_amount_in_transaction(trans)
        trans.refresh_from_db()
        if unpaid_amount <= 0:
            continue

        remaining_amount = trans.remaining_amount

        if unpaid_amount <= remaining_amount:
            trans.remaining_amount = remaining_amount - unpaid_amount
            TransactionSaleDocumentPayment.objects.create(
                transaction=transaction, sale_document=sale_document, amount_paid=remaining_amount - unpaid_amount
            )
            unpaid_amount = 0
            trans.save()
        else:
            TransactionSaleDocumentPayment.objects.create(
                transaction=transaction, sale_document=sale_document, amount_paid=remaining_amount
            )
            trans.remaining_amount = 0
            trans.save()
            unpaid_amount -= remaining_amount


def update_amount_paid_document(document, amount_paid, payment_status):
    document.amount_paid = amount_paid
    document.payment_status = payment_status
    document.skip_child_validation_form_transaction = True
    document.save()
    document.skip_child_validation_form_transaction = False


def update_remaining_amount_in_transaction(transaction):
    transactions = transaction.transactionsaledocumentpayment_set.all()
    amount_paid = sum(tr.amount_paid for tr in transactions)
    transaction.remaining_amount = transaction.amount - amount_paid
    transaction.save()


def handle_amount_paid_and_status_paid_sale_document(sale_document):
    transactions = sale_document.transactionsaledocumentpayment_set.all()
    amount_paid = sum(tr.amount_paid for tr in transactions)

    sale_document.amount_paid = amount_paid

    if sale_document.amount_paid == sale_document.total_amount:
        sale_document.payment_status = SaleDocumentPaymentStatus.PAID.name
    elif sale_document.amount_paid > 0:
        sale_document.payment_status = SaleDocumentPaymentStatus.PARTIAL_PAID.name
    else:
        sale_document.payment_status = SaleDocumentPaymentStatus.NOT_PAID.name

    sale_document.skip_child_validation_form_transaction = True
    sale_document.save()
    sale_document.skip_child_validation_form_transaction = False
