import csv
import logging
from datetime import datetime
from io import BytesIO
from uuid import UUID

import openpyxl
from common.enums.partner_type import PartnerType
from common.enums.purchase_document_enum import PurchaseDocumentPaymentStatus
from common.enums.purchase_document_enum import PurchaseDocumentStatus
from common.enums.sale_document_enum import SaleDocumentStatus
from common.enums.sale_document_enum import SaleDocumentTypes
from common.service.purchase_sale_service import SalePurchaseService
from django.db.models import Sum
from django.http import HttpResponse
from django.utils import timezone
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

    @staticmethod
    def expected_amount_by_due_date():
        current_date = timezone.now().date()

        expected_amounts = {
            'expected_in_3_days': 0,
            'expected_in_7_days': 0,
            'expected_in_15_days': 0,
            'expected_in_1_month': 0
        }

        documents = BimaErpPurchaseDocument.objects.filter(
            type=SaleDocumentTypes.INVOICE.name,
            status=SaleDocumentStatus.CONFIRMED.name
        )

        for document in documents:
            amount_due = document.total_amount - document.calculate_sum_amount_paid()

            if amount_due <= 0:
                continue
            if not document.payment_terms:
                continue

            due_dates = SalePurchaseService.get_due_dates_based_on_payment_terms(document)

            for due_date in due_dates:
                SalePurchaseService.classify_and_sum_due_amounts(expected_amounts, due_date, current_date, amount_due)

        return expected_amounts


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


def duplicate_purchase_document_service(parents):
    new_created_documents = []
    for sale_doc in parents:
        parent_values = BimaErpPurchaseDocument.objects.filter(id=sale_doc.id).values().first()
        del parent_values['id']
        del parent_values['public_id']
        del parent_values['number']
        del parent_values['date']
        del parent_values['status']
        del parent_values['amount_paid']
        del parent_values['payment_status']

        parent_values['number'] = SalePurchaseService.generate_unique_number('sale', sale_doc.type.lower())
        parent_values['date'] = timezone.now().date()
        parent_values['status'] = SaleDocumentStatus.DRAFT.name
        parent_values['next_due_date'] = None
        parent_values['is_payment_late'] = False
        parent_values['days_in_late'] = 0
        parent_values['last_due_date'] = None
        parent_values['amount_paid'] = 0
        parent_values['payment_status'] = PurchaseDocumentPaymentStatus.NOT_PAID.name

        new_document = BimaErpPurchaseDocument.objects.create(**parent_values)
        create_products_from_parents([sale_doc], new_document)

        new_created_documents.append(new_document)

    return new_created_documents


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
                    elif field.name == 'payment_terms':
                        value = purchase_document.payment_terms.name if purchase_document.payment_terms is not None else ''
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
