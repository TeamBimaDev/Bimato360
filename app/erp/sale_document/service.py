import csv
import logging
from datetime import datetime
from io import BytesIO
from uuid import UUID

import openpyxl
from common.enums.partner_type import PartnerType
from common.enums.sale_document_enum import SaleDocumentRecurringCycle
from common.enums.sale_document_enum import SaleDocumentRecurringIntervalCustomUnit
from common.enums.sale_document_enum import SaleDocumentStatus
from common.enums.sale_document_enum import time_interval_based_on_recurring_interval, SaleDocumentRecurringInterval
from common.service.purchase_sale_service import SalePurchaseService
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from erp.sale_document.models import BimaErpSaleDocument
from pandas import DataFrame

from .models import BimaErpSaleDocument, BimaErpSaleDocumentProduct, update_sale_document_totals

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
    today = datetime.today().date()
    num_new_sale_documents = 0

    recurring_sale_documents = BimaErpSaleDocument.objects.filter(
        is_recurring=True,
        recurring_initial_parent_id=None,
        recurring_initial_parent_public_id=None,
        is_recurring_parent=True,
        is_recurring_ended=False,
        status=SaleDocumentStatus.CONFIRMED.name
    )

    for sale_document in recurring_sale_documents:
        recurring_interval_time = get_recurring_interval_value(sale_document)
        if recurring_interval_time is None:
            continue

        if sale_document.recurring_next_generated_day is None:
            sale_document.recurring_next_generated_day = sale_document.date + recurring_interval_time
            sale_document.save()

        if sale_document.recurring_next_generated_day <= today:
            try:
                if not verify_recurring_not_ended(sale_document):
                    continue
                if not verify_recurring_limit_number_not_attempt(sale_document):
                    continue

                logger.info(f"Treating sale document number: {sale_document.number}")

                with transaction.atomic():
                    initial_parent_id = sale_document.id
                    initial_parent_public_id = sale_document.public_id

                    new_sale_document = create_new_document(
                        document_type=sale_document.type,
                        parents=[sale_document],
                        initial_recurrent_parent_id=initial_parent_id,
                        initial_recurrent_parent_public_id=initial_parent_public_id,
                        is_recurring=True
                    )

                    create_products_from_parents(parents=[sale_document], new_document=new_sale_document)

                    logger.info(
                        f"{new_sale_document.type} N° {new_sale_document.number} is created from {sale_document.number}")
                    num_new_sale_documents += 1

            except Exception as e:
                logger.error(f"Error creating new SaleDocument for parent {sale_document.id}: {str(e)}")

            sale_document.recurring_next_generated_day = today + recurring_interval_time
            sale_document.recurring_last_generated_day = today
            sale_document.save()

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


def create_new_document(document_type, parents, initial_recurrent_parent_id=None,
                        initial_recurrent_parent_public_id=None, is_recurring=False):
    new_document = BimaErpSaleDocument.objects.create(
        number=SalePurchaseService.generate_unique_number('sale', document_type.lower()),
        date=datetime.today().strftime('%Y-%m-%d'),
        status=SaleDocumentStatus.DRAFT.name,
        type=document_type,
        partner=parents[0].partner,
        recurring_initial_parent_id=initial_recurrent_parent_id,
        recurring_initial_parent_public_id=initial_recurrent_parent_public_id,
        is_recurring=is_recurring
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
    for sale_document in data:
        try:
            row = {}
            for field in fields:
                value = None
                try:
                    if field.name == 'partner':
                        partner = sale_document.partner
                        value = partner.company_name if partner.partner_type == PartnerType.COMPANY.name else \
                            f"{partner.first_name} {partner.last_name}"
                    elif field.choices:
                        value = getattr(sale_document, f"get_{field.name}_display")()
                    else:
                        value = getattr(sale_document, field.name)

                    if isinstance(value, UUID):
                        value = str(value)
                    elif isinstance(value, datetime):
                        value = value.replace(tzinfo=None)

                    row[field.name] = value
                except Exception as e:
                    logger.error(f"Error processing field {field.name} for object {sale_document.pk}: {e}")
            rows.append(row)
        except Exception as e:
            logger.error(f"Error processing object {sale_document.pk}: {e}")
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
    response['Content-Disposition'] = 'attachment; filename="sales.csv"'
    field_name_to_show = [fd.name for fd in fields]
    writer = csv.writer(response)
    writer.writerow(field_name_to_show)

    for sale_document in data:
        row_data = []
        for field in fields:
            try:
                if field.name == "partner":
                    partner = sale_document.partner
                    value = partner.company_name if partner.partner_type == PartnerType.COMPANY.name else \
                        f"{partner.first_name} {partner.last_name}"
                elif field.choices:
                    value = getattr(sale_document, f"get_{field.name}_display")()
                else:
                    value = getattr(sale_document, field.name)
                row_data.append(value if value is not None else '')
            except Exception as e:
                logger.error(f"Error writing row {sale_document.id} to CSV file: {e}")
                continue
        writer.writerow(row_data)

    return response


def get_recurring_interval_value(sale_document):
    recurring_interval_time = time_interval_based_on_recurring_interval.get(sale_document.recurring_interval, None)

    if recurring_interval_time is None and \
            sale_document.recurring_interval == SaleDocumentRecurringInterval.CUSTOM.name:
        recurring_interval_time = get_custom_recurring_interval_value(
            sale_document.recurring_interval_type_custom_unit, sale_document.recurring_interval_type_custom_number)

    return recurring_interval_time


def get_custom_recurring_interval_value(unit, number):
    time_interval_based_on_recurring_interval_custom_unit = {
        SaleDocumentRecurringIntervalCustomUnit.DAY.name: relativedelta(days=number),
        SaleDocumentRecurringIntervalCustomUnit.WEEK.name: relativedelta(weeks=number),
        SaleDocumentRecurringIntervalCustomUnit.MONTH.name: relativedelta(months=number),
        SaleDocumentRecurringIntervalCustomUnit.YEAR.name: relativedelta(years=number),
    }
    return time_interval_based_on_recurring_interval_custom_unit.get(unit, None)


def verify_recurring_not_ended(sale_document):
    if sale_document.recurring_cycle != SaleDocumentRecurringCycle.END_AT.name:
        return True
    if sale_document.recurring_cycle_stop_at > datetime.now().date():
        return True

    stop_recurring_sale_document(sale_document, sale_document.recurring_cycle_stop_at)
    logger.error(
        f"Recurring sale document N° {sale_document.public_id} ended at {sale_document.recurring_cycle_stop_at} "
        f"current date is {datetime.now()}")
    return False


def verify_recurring_limit_number_not_attempt(sale_document):
    if sale_document.recurring_cycle != SaleDocumentRecurringCycle.END_AFTER.name:
        return True

    recurring_times_number = get_number_recurrent_document_generated_from_parent(sale_document)
    if recurring_times_number < sale_document.recurring_cycle_number_to_repeat:
        return True

    stop_recurring_sale_document(sale_document, datetime.now())
    logger.error(
        f"Recurring sale document N° {sale_document.public_id} ended at {sale_document.recurring_cycle_stop_at} "
        f"after recurring {recurring_times_number} times ")
    return False


def get_number_recurrent_document_generated_from_parent(sale_document):
    return BimaErpSaleDocument.objects.filter(initial_parent_public_id=sale_document.public_id,
                                              is_recurring=True).count()


def stop_recurring_sale_document(sale_document, stop_date, reason=None, stopped_by=False, request=None):
    try:
        sale_document.recurring_cycle_stopped_at = stop_date
        sale_document.is_recurring_ended = True
        sale_document.recurring_reason_stop = reason
        if stopped_by:
            user = None
            if request and hasattr(request, "user"):
                user = request.user
            sale_document.recurring_stopped_by = user

        sale_document.recurring_reason_reactivated = None
        sale_document.recurring_reactivated_by = None
        sale_document.recurring_reactivated_date = None
        sale_document.save()
        return True
    except Exception as ex:
        logger.error(f"Unable to stop sale_document {sale_document.public_id} for reason {ex.args}")
        return False


def reactivate_recurring_sale_document(sale_document, reactivation_date, reason=None, reactivated_by=False,
                                       request=None):
    try:
        sale_document.recurring_reactivated_date = reactivation_date
        sale_document.recurring_reason_reactivated = reason
        if reactivated_by:
            user = None
            if request and hasattr(request, "user"):
                user = request.user
            sale_document.recurring_reactivated_by = user

        sale_document.recurring_stopped_by = None
        sale_document.recurring_reason_stop = None
        sale_document.is_recurring_ended = False
        sale_document.recurring_cycle_stopped_at = None

        sale_document.save()
        return True
    except Exception as ex:
        logger.error(f"Unable to reactivate sale_document {sale_document.public_id} for reason {ex.args}")
        return False
