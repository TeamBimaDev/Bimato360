from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from erp.sale_document.models import BimaErpSaleDocument

from common.service.purchase_sale_service import SalePurchaseService


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
