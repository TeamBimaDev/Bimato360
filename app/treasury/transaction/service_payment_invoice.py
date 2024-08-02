from common.enums.purchase_document_enum import PurchaseDocumentPaymentStatus, PurchaseDocumentStatus, \
    PurchaseDocumentTypes
from common.enums.sale_document_enum import SaleDocumentPaymentStatus, SaleDocumentStatus, SaleDocumentTypes
from common.enums.transaction_enum import TransactionTypeIncomeOutcome
from django.apps import apps
from django.db import transaction as db_transaction
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


def handle_invoice_payment(transaction, document_public_ids):
    if transaction.transaction_type.code in _get_invoice_payment_customer_codes():
        handle_invoice_payment_customer_invoice(transaction, document_public_ids)
    elif transaction.transaction_type.code in _get_invoice_payment_supplier_codes():
        handle_invoice_payment_supplier_invoice(transaction, document_public_ids)
    else:
        return


def handle_credit_note_payment(transaction, document_public_ids):
    if transaction.transaction_type.code in _get_credit_note_payment_codes():
        handle_credit_note_payment_invoice(transaction, document_public_ids)
    else:
        return


def get_total_amount_used_for_transaction(transaction):
    if transaction.direction == TransactionTypeIncomeOutcome.INCOME.name:
        transactions = transaction.transactionsaledocumentpayment_set.all()
    else:
        transactions = transaction.transactionpurchasedocumentpayment_set.all()

    amount_paid = sum(tr.amount_paid for tr in transactions)

    return transaction.amount - amount_paid


def handle_credit_note_payment_invoice(transaction, document_public_ids):
    BimaErpSaleDocument = apps.get_model('erp', 'BimaErpSaleDocument')
    TransactionSaleDocumentPayment = apps.get_model('treasury', 'TransactionSaleDocumentPayment')
    sale_documents = BimaErpSaleDocument.objects.filter(
        public_id__in=document_public_ids
    ).order_by('date', 'id')

    sum_sale_document_amount = _get_sum_sale_document_amount(sale_documents)
    if sum_sale_document_amount != transaction.amount:
        raise ValidationError({"Error": _("Amount of the transaction should be equal to the amount of credit note!")})

    delete_old_paid_transaction_sale_document(transaction)

    remaining_amount = transaction.amount

    for doc in sale_documents:
        if not doc.status == SaleDocumentStatus.CONFIRMED.name and not doc.status == SaleDocumentTypes.CREDIT_NOTE.name:
            continue

        _update_amount_paid_sale_document(doc)
        doc.refresh_from_db()
        if remaining_amount <= 0:
            continue

        unpaid_amount = doc.total_amount - doc.amount_paid

        if unpaid_amount <= remaining_amount:
            doc.payment_status = SaleDocumentPaymentStatus.PAID.name
            doc.amount_paid += unpaid_amount
            TransactionSaleDocumentPayment.objects.create(
                transaction=transaction, sale_document=doc, amount_paid=unpaid_amount
            )
            remaining_amount -= unpaid_amount
        else:
            doc.payment_status = SaleDocumentPaymentStatus.PARTIAL_PAID.name
            doc.amount_paid += remaining_amount
            TransactionSaleDocumentPayment.objects.create(
                transaction=transaction, sale_document=doc, amount_paid=remaining_amount
            )
            remaining_amount = 0

        doc.skip_child_validation_form_transaction = True
        doc.save()
        doc.skip_child_validation_form_transaction = False

    transaction.remaining_amount = remaining_amount
    transaction.save()


def handle_invoice_payment_customer_invoice(transaction, document_public_ids):
    BimaErpSaleDocument = apps.get_model('erp', 'BimaErpSaleDocument')
    TransactionSaleDocumentPayment = apps.get_model('treasury', 'TransactionSaleDocumentPayment')
    delete_old_paid_transaction_sale_document(transaction)

    remaining_amount = transaction.amount
    sale_documents = BimaErpSaleDocument.objects.filter(
        public_id__in=document_public_ids
    ).order_by('date', 'id')

    for doc in sale_documents:
        if not doc.status == SaleDocumentStatus.CONFIRMED.name and not doc.type == SaleDocumentTypes.INVOICE.name:
            continue

        _update_amount_paid_sale_document(doc)
        doc.refresh_from_db()
        if remaining_amount <= 0:
            continue

        unpaid_amount = doc.total_amount - doc.amount_paid

        if unpaid_amount <= remaining_amount:
            doc.payment_status = SaleDocumentPaymentStatus.PAID.name
            doc.amount_paid += unpaid_amount
            TransactionSaleDocumentPayment.objects.create(
                transaction=transaction, sale_document=doc, amount_paid=unpaid_amount
            )
            remaining_amount -= unpaid_amount
        else:
            doc.payment_status = SaleDocumentPaymentStatus.PARTIAL_PAID.name
            doc.amount_paid += remaining_amount
            TransactionSaleDocumentPayment.objects.create(
                transaction=transaction, sale_document=doc, amount_paid=remaining_amount
            )
            remaining_amount = 0

        doc.skip_child_validation_form_transaction = True
        doc.save()
        doc.skip_child_validation_form_transaction = False

    transaction.remaining_amount = remaining_amount
    transaction.save()


def handle_invoice_payment_supplier_invoice(transaction, document_public_ids):
    BimaErpPurchaseDocument = apps.get_model('erp', 'BimaErpPurchaseDocument')
    TransactionPurchaseDocumentPayment = apps.get_model('treasury', 'TransactionPurchaseDocumentPayment')
    _delete_old_paid_transaction_purchase_document(transaction)

    remaining_amount = transaction.amount
    purchase_documents = BimaErpPurchaseDocument.objects.filter(
        public_id__in=document_public_ids
    ).order_by('date', 'id')

    for doc in purchase_documents:
        if not doc.status == PurchaseDocumentStatus.CONFIRMED.name and not doc.type == PurchaseDocumentTypes.INVOICE.name:
            continue
        _update_amount_paid_purchase_document(doc)
        doc.refresh_from_db()
        if remaining_amount <= 0:
            continue

        unpaid_amount = doc.total_amount - doc.amount_paid

        if unpaid_amount <= remaining_amount:
            doc.payment_status = PurchaseDocumentPaymentStatus.PAID.name
            doc.amount_paid += unpaid_amount
            TransactionPurchaseDocumentPayment.objects.create(
                transaction=transaction, purchase_document=doc, amount_paid=unpaid_amount
            )
            remaining_amount -= unpaid_amount
        else:
            doc.payment_status = PurchaseDocumentPaymentStatus.PARTIAL_PAID.name
            doc.amount_paid += remaining_amount
            TransactionPurchaseDocumentPayment.objects.create(
                transaction=transaction, purchase_document=doc, amount_paid=remaining_amount
            )
            remaining_amount = 0

        doc.skip_child_validation_form_transaction = True
        doc.save()
        doc.skip_child_validation_form_transaction = False

    transaction.remaining_amount = remaining_amount
    transaction.save()


def handle_invoice_payment_deletion(transaction_paid):
    if transaction_paid.transaction_type.code in _get_invoice_payment_customer_codes():
        delete_old_paid_transaction_sale_document(transaction_paid)
    elif transaction_paid.transaction_type.code in _get_invoice_payment_supplier_codes():
        _delete_old_paid_transaction_purchase_document(transaction_paid)


def _update_amount_paid_sale_document(sale_document):
    transactions = sale_document.transactionsaledocumentpayment_set.all()
    _update_amount_paid_document(sale_document, transactions, SaleDocumentPaymentStatus)


def _update_amount_paid_purchase_document(purchase_document):
    transactions = purchase_document.transactionpurchasedocumentpayment_set.all()
    _update_amount_paid_document(purchase_document, transactions, PurchaseDocumentPaymentStatus)


def delete_old_paid_transaction_sale_document(transaction_paid):
    with db_transaction.atomic():
        TransactionSaleDocumentPayment = apps.get_model('treasury', 'TransactionSaleDocumentPayment')
        old_sale_document_payments = TransactionSaleDocumentPayment.objects.filter(transaction=transaction_paid)
        old_sale_documents = [payment.sale_document for payment in old_sale_document_payments]
        old_sale_document_payments.delete()
        for sale_doc in old_sale_documents:
            _update_amount_paid_sale_document(sale_doc)


def _delete_old_paid_transaction_purchase_document(transaction_paid):
    with db_transaction.atomic():
        TransactionPurchaseDocumentPayment = apps.get_model('treasury', 'TransactionPurchaseDocumentPayment')
        old_purchase_document_payments = TransactionPurchaseDocumentPayment.objects.filter(
            transaction=transaction_paid)
        old_purchase_documents = [payment.purchase_document for payment in old_purchase_document_payments]
        old_purchase_document_payments.delete()
        for purchase_doc in old_purchase_documents:
            _update_amount_paid_purchase_document(purchase_doc)


def _update_amount_paid_document(document, transactions, payment_status):
    amount_paid = sum(tr.amount_paid for tr in transactions)

    document.amount_paid = amount_paid

    if document.amount_paid == document.total_amount:
        document.payment_status = payment_status.PAID.name
        document.is_payment_late = False
        document.days_in_late = 0
    elif document.amount_paid > 0:
        document.payment_status = payment_status.PARTIAL_PAID.name
    else:
        document.payment_status = payment_status.NOT_PAID.name
    document.skip_child_validation_form_transaction = True
    document.save()
    document.skip_child_validation_form_transaction = False


def _get_sum_sale_document_amount(sale_documents):
    return sum(sd.total_amount for sd in sale_documents)


def _get_invoice_payment_codes():
    return ["INVOICE_PAYMENT_CASH", "INVOICE_PAYMENT_BANK", "INVOICE_PAYMENT_OUTCOME_BANK",
            "INVOICE_PAYMENT_OUTCOME_CASH"]


def _get_invoice_payment_customer_codes():
    return ["INVOICE_PAYMENT_CASH", "INVOICE_PAYMENT_BANK"]


def _get_invoice_payment_supplier_codes():
    return ["INVOICE_PAYMENT_OUTCOME_BANK", "INVOICE_PAYMENT_OUTCOME_CASH"]


def _get_credit_note_payment_codes():
    return ["CREDIT_NOTE_OUTCOME_BANK", "CREDIT_NOTE_OUTCOME_CASH"]
