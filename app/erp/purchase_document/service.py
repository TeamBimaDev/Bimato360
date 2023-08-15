import csv
import logging
from datetime import datetime
from io import BytesIO
from uuid import UUID

import openpyxl
from common.enums.partner_type import PartnerType
from common.enums.purchase_document_enum import PurchaseDocumentStatus
from common.service.purchase_sale_service import SalePurchaseService
from django.db.models import Sum
from django.http import HttpResponse
from pandas import DataFrame

from .models import BimaErpPurchaseDocument, BimaErpPurchaseDocumentProduct, update_purchase_document_totals

logger = logging.getLogger(__name__)


class PurchaseDocumentService:

    @staticmethod
    def get_unique_number(request, **kwargs):
        sale_or_purchase = kwargs.get('sale_purchase', '')
        quotation_order_invoice = kwargs.get('quotation_order_invoice', '')
        if not sale_or_purchase:
            sale_or_purchase = request.query_params.get('sale_purchase', '')
        if not quotation_order_invoice:
            quotation_order_invoice = request.query_params.get('quotation_order_invoice', '')

        SalePurchaseService.validate_data(sale_or_purchase, quotation_order_invoice)

        unique_number = SalePurchaseService.generate_unique_number(sale_or_purchase, quotation_order_invoice)
        while BimaErpPurchaseDocument.objects.filter(number=unique_number).exists():
            unique_number = SalePurchaseService.generate_unique_number(sale_or_purchase,
                                                                       quotation_order_invoice)
        return unique_number


def create_products_from_parents(parents, new_document, reset_quantity=False):
    product_ids = BimaErpPurchaseDocumentProduct.objects.filter(
        purchase_document__in=parents
    ).values_list('product', flat=True).distinct()

    new_products = []
    for product_id in product_ids:
        # Find first instance of this product
        first_product = BimaErpPurchaseDocumentProduct.objects.filter(
            purchase_document__in=parents,
            product_id=product_id
        ).first()

        if first_product is None:
            continue

        total_quantity = BimaErpPurchaseDocumentProduct.objects.filter(
            purchase_document__in=parents,
            product_id=product_id
        ).aggregate(total_quantity=Sum('quantity'))['total_quantity']

        new_product = BimaErpPurchaseDocumentProduct(
            purchase_document=new_document,
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

    BimaErpPurchaseDocumentProduct.objects.bulk_create(new_products)
    update_purchase_document_totals(new_document)
    new_document.save()


def create_new_document(document_type, parents):
    new_document = BimaErpPurchaseDocument.objects.create(
        number=SalePurchaseService.generate_unique_number('purchase', document_type.lower()),
        date=datetime.today().strftime('%Y-%m-%d'),
        status=PurchaseDocumentStatus.DRAFT.name,
        type=document_type,
        partner=parents[0].partner,
    )
    new_document.parents.add(*parents)
    return new_document


def calculate_totals_for_selected_items(items):
    sums = items.aggregate(
        total_amount_without_vat=Sum('total_amount_without_vat'),
        total_vat=Sum('total_vat'),
        total_discount=Sum('total_discount'),
        total_after_discount=Sum('total_after_discount'),
        total_amount=Sum('total_amount')
    )
    total_amount_without_vat = sums['total_amount_without_vat']
    total_vat = sums['total_vat']
    total_discount = sums['total_discount']
    total_after_discount = sums['total_after_discount']
    total_amount = sums['total_amount']
    totals = {
        'total_amount_without_vat': total_amount_without_vat,
        'total_vat': total_vat,
        'total_discount': total_discount,
        'total_after_discount': total_after_discount,
        'total_amount': total_amount
    }
    return totals


def generate_xls_report(data, fields):
    rows = []
    for purchase_document in data:
        try:
            row = {}
            for field in fields:
                value = None
                try:
                    if field.name == 'partner':
                        partner = purchase_document.partner
                        value = partner.company_name if partner.partner_type == PartnerType.COMPANY.name else \
                            f"{partner.first_name} {partner.last_name}"
                    elif field.choices:
                        value = getattr(purchase_document, f"get_{field.name}_display")()
                    else:
                        value = getattr(purchase_document, field.name)

                    if isinstance(value, UUID):
                        value = str(value)
                    elif isinstance(value, datetime):
                        value = value.replace(tzinfo=None)

                    row[field.name] = value
                except Exception as e:
                    logger.error(f"Error processing field {field.name} for object {purchase_document.pk}: {e}")
            rows.append(row)
        except Exception as e:
            logger.error(f"Error processing object {purchase_document.pk}: {e}")
            continue

    try:
        df = DataFrame(rows)

        wb = openpyxl.Workbook()
        ws = wb.active

        headers = [str(field.verbose_name) for field in fields]
        ws.append(headers)

        for r in DataFrame(df).iterrows():
            try:
                ws.append(r[1].tolist())
            except Exception as e:
                logger.error(f"Error writing row {r[0]} to Excel file: {e}")
                continue

        excel_file = BytesIO()
        wb.save(excel_file)

        response = HttpResponse(
            excel_file.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=export.xlsx'

        return response

    except Exception as e:
        logger.error(f"Error generating Excel file: {e}")
        raise e


def generate_csv_report(data, fields):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="purchases.csv"'
    field_name_to_show = [fd.name for fd in fields]
    writer = csv.writer(response)
    writer.writerow(field_name_to_show)

    for purchase_document in data:
        row_data = []
        for field in fields:
            try:
                if field.name == "partner":
                    partner = purchase_document.partner
                    value = partner.company_name if partner.partner_type == PartnerType.COMPANY.name else \
                        f"{partner.first_name} {partner.last_name}"
                elif field.choices:
                    value = getattr(purchase_document, f"get_{field.name}_display")()
                else:
                    value = getattr(purchase_document, field.name)
                row_data.append(value if value is not None else '')
            except Exception as e:
                logger.error(f"Error writing row {purchase_document.id} to CSV file: {e}")
                continue
        writer.writerow(row_data)

    return response
