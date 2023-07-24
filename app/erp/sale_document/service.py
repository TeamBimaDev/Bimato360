from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from erp.sale_document.models import BimaErpSaleDocument

from datetime import datetime, timedelta
from django.db import transaction
from django.db.models import Sum

from .models import BimaErpSaleDocument, BimaErpSaleDocumentProduct, update_sale_document_totals
import logging
from django.utils.translation import gettext as _

from common.enums.sale_document_enum import SaleDocumentStatus
from common.service.purchase_sale_service import SalePurchaseService

logger = logging.getLogger(__name__)


class SaleDocumentService:

    @staticmethod
    def validate_data(sale_or_purchase, quotation_order_invoice):
        if not sale_or_purchase or not quotation_order_invoice:
            raise ValidationError(_('Please provide all needed data'))

    @staticmethod
    def get_unique_number(request, **kwargs):
        sale_or_purchase = kwargs.get('sale_purchase', '')
        quotation_order_invoice = kwargs.get('quotation_order_invoice', '')
        if not sale_or_purchase:
            sale_or_purchase = request.query_params.get('sale_purchase', '')
        if not quotation_order_invoice:
            quotation_order_invoice = request.query_params.get('quotation_order_invoice', '')

        SaleDocumentService.validate_data(sale_or_purchase, quotation_order_invoice)

        unique_number = SalePurchaseService.generate_unique_number(sale_or_purchase, quotation_order_invoice)
        while BimaErpSaleDocument.objects.filter(number=unique_number).exists():
            unique_number = SalePurchaseService.generate_unique_number(sale_or_purchase, quotation_order_invoice)
        return unique_number


def generate_recurring_sale_documents():
    today = datetime.today()
    num_new_sale_documents = 0

    recurring_sale_documents = BimaErpSaleDocument.objects.filter(is_recurring=True)

    for sale_document in recurring_sale_documents:
        logger.info(f"Treating sale document number: {sale_document.number}")

        next_creation_date = sale_document.date + timedelta(days=sale_document.recurring_interval)

        if next_creation_date <= today:
            try:
                with transaction.atomic():
                    new_sale_document = create_new_document(
                        document_type=sale_document.type,
                        parents=[sale_document]
                    )
                    create_products_from_parents(parents=[sale_document], new_document=new_sale_document)

                    logger.info(
                        f"{new_sale_document.type} N° {new_sale_document.number}"
                        f" is created from {sale_document.number}")

                    num_new_sale_documents += 1

            except Exception as e:
                logger.error(_(f"Error creating new SaleDocument for parent {sale_document.id}: {str(e)}"))

    logger.info(f'Successfully created {num_new_sale_documents} new sale documents')


def create_products_from_parents(parents, new_document, reset_quantity=False):
    product_ids = BimaErpSaleDocumentProduct.objects.filter(
        sale_document__in=parents
    ).values_list('product', flat=True).distinct()

    new_products = []
    for product_id in product_ids:
        # Find first instance of this product
        first_product = BimaErpSaleDocumentProduct.objects.filter(
            sale_document__in=parents,
            product_id=product_id
        ).first()

        if first_product is None:
            continue

        total_quantity = BimaErpSaleDocumentProduct.objects.filter(
            sale_document__in=parents,
            product_id=product_id
        ).aggregate(total_quantity=Sum('quantity'))['total_quantity']

        new_product = BimaErpSaleDocumentProduct(
            sale_document=new_document,
            name=first_product.name,
            unit_of_measure=first_product.unit_of_measure,
            reference=first_product.reference,
            product_id=product_id,
            quantity=1 if reset_quantity else total_quantity,
            unit_price=first_product.unit_price,
            vat=first_product.vat,
            description=first_product.description,
            discount=first_product.discount
        )
        new_product.calculate_totals()
        new_products.append(new_product)

    BimaErpSaleDocumentProduct.objects.bulk_create(new_products)
    update_sale_document_totals(new_document)
    new_document.save()


def create_new_document(document_type, parents):
    new_document = BimaErpSaleDocument.objects.create(
        number=SalePurchaseService.generate_unique_number('sale', document_type.lower()),
        date=datetime.today().strftime('%Y-%m-%d'),
        status=SaleDocumentStatus.DRAFT.name,
        type=document_type,
        partner=parents.first().partner,
    )
    new_document.parents.add(*parents)
    return new_document
