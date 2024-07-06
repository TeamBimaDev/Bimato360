import logging

from common.enums.purchase_document_enum import PurchaseDocumentTypes, PurchaseDocumentPaymentStatus, \
    PurchaseDocumentStatus
from common.enums.transaction_enum import PaymentTermType
from common.service.purchase_sale_service import SalePurchaseService
from django.apps import apps

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
                SalePurchaseService.calculate_payment_late_type_not_custom(purchase_document)
            else:
                SalePurchaseService.calculate_payment_late_type_custom(purchase_document)
            purchase_document_to_return.append(
                {"purchase_document_public_ud": purchase_document.public_id,
                 "next_due_date": purchase_document.next_due_date})
            logger.info(f"purchase document verification {purchase_document.public_id} succeeded")
            print(f"purchase document verification {purchase_document.public_id} succeeded")
        except Exception as ex:
            logger.error(f"purchase document verification {purchase_document.public_id} faild {ex}")
            print(f"purchase document verification {purchase_document.public_id} faild {ex}")

    return purchase_document_to_return
