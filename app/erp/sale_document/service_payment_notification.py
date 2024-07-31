<<<<<<< HEAD
import logging

from common.enums.sale_document_enum import SaleDocumentTypes, SaleDocumentPaymentStatus, SaleDocumentStatus
from common.enums.transaction_enum import PaymentTermType
from common.service.purchase_sale_service import SalePurchaseService
from django.apps import apps

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
                SalePurchaseService.calculate_payment_late_type_not_custom(sale_document)
            else:
                SalePurchaseService.calculate_payment_late_type_custom(sale_document)
            sale_document_to_return.append(
                {"sale_document_public_ud": sale_document.public_id, "next_due_date": sale_document.next_due_date})
            logger.info(f"sale document verification {sale_document.public_id} succeeded")
            print(f"sale document verification {sale_document.public_id} succeeded")
        except Exception as ex:
            logger.error(f"sale document verification {sale_document.public_id} faild {ex}")
            print(f"sale document verification {sale_document.public_id} faild {ex}")

    return sale_document_to_return
=======
import logging

from common.enums.sale_document_enum import SaleDocumentTypes, SaleDocumentPaymentStatus, SaleDocumentStatus
from common.enums.transaction_enum import PaymentTermType
from common.service.purchase_sale_service import SalePurchaseService
from django.apps import apps

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
                SalePurchaseService.calculate_payment_late_type_not_custom(sale_document)
            else:
                SalePurchaseService.calculate_payment_late_type_custom(sale_document)
            sale_document_to_return.append(
                {"sale_document_public_ud": sale_document.public_id, "next_due_date": sale_document.next_due_date})
            logger.info(f"sale document verification {sale_document.public_id} succeeded")
            print(f"sale document verification {sale_document.public_id} succeeded")
        except Exception as ex:
            logger.error(f"sale document verification {sale_document.public_id} faild {ex}")
            print(f"sale document verification {sale_document.public_id} faild {ex}")

    return sale_document_to_return
>>>>>>> origin/ma-branch
