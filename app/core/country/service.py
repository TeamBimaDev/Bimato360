import csv
from django.db.models import Q, ForeignKey
from .models import BimaCoreCountry
from core.currency.models import BimaCoreCurrency
import pandas as pd
from django.db import transaction, IntegrityError, models
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from pandas import DataFrame
import openpyxl
from io import BytesIO
from uuid import UUID
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def import_data_from_csv_file(df):
    error_rows = []
    created_count = 0

    for index, row in df.iterrows():
        try:
            # Validate and clean data
            name = str(row.get('name', '')) if pd.notna(row.get('name')) else ""
            code = str(row.get('code', '')) if pd.notna(row.get('code')) else ""
            iso3 = str(row.get('iso3', '')) if pd.notna(row.get('iso3')) else ""
            iso2 = str(row.get('iso2', '')) if pd.notna(row.get('iso2')) else ""
            phone_code = str(row.get('phone_code', '')) if pd.notna(row.get('phone_code')) else ""
            capital = str(row.get('capital', '')) if pd.notna(row.get('capital')) else ""
            address_format = str(row.get('address_format', '')) if pd.notna(row.get('address_format')) else ""
            vat_label = str(row.get('vat_label', '')) if pd.notna(row.get('vat_label')) else ""
            zip_required = bool(row.get('zip_required', False)) if pd.notna(row.get('zip_required')) else False
            currency_name_or_symbol = str(row.get('currency', '')) if pd.notna(row.get('currency')) else ""

            # Check if mandatory fields are provided
            if not name:
                error_rows.append({'error': _('Name is missing'), 'data': name if name else ""})
                continue
            if not code:
                error_rows.append({'error': _('Code is missing'), 'data': name if name else ""})
                continue

            # Check if currency exists
            currency = BimaCoreCurrency.objects.filter(
                Q(name=currency_name_or_symbol) | Q(symbol=currency_name_or_symbol)).first()
            if not currency:
                error_rows.append(
                    {'error': _('Currency with name or symbol {} does not exist').format(currency_name_or_symbol),
                     'data': name if name else ""})
                continue

            # Create the object
            with transaction.atomic():
                BimaCoreCountry.objects.create(
                    name=name,
                    code=code,
                    iso3=iso3,
                    iso2=iso2,
                    phone_code=phone_code,
                    capital=capital,
                    address_format=address_format,
                    vat_label=vat_label,
                    zip_required=zip_required,
                    currency=currency
                )
            created_count += 1
        except IntegrityError as e:
            if 'name' in str(e):
                error_message = _('Country with name {} already exists').format(name if name else "")
            elif 'code' in str(e):
                error_message = _('Country with code {} already exists').format(code if code else "")
            else:
                error_message = _('Integrity error occurred')
            error_rows.append({'error': error_message, 'data': name if name else ""})
        except Exception as e:
            error_rows.append({'error': str(e), 'data': name if name else ""})

    return error_rows, created_count


def export_to_csv(countries, model_fields):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    field_names_to_show = [fd.name for fd in model_fields.fields]
    writer = csv.writer(response)
    writer.writerow(field_names_to_show)

    for country in countries:
        row_data = []
        for field in field_names_to_show:
            try:
                value = getattr(country, field)
                if hasattr(value, 'name'):
                    value = getattr(value, 'name', None)
                row_data.append(value if value is not None else '')
            except Exception as ex:
                pass
        writer.writerow(row_data)

    return response


def generate_xls_file(queryset):
    rows = []
    for obj in queryset:
        row = {}
        for field in obj._meta.fields:
            field_value = getattr(obj, field.name)

            if isinstance(field, models.ForeignKey):
                if field_value is not None:
                    field_value = getattr(field_value, 'name', '')

            elif isinstance(field_value, datetime):
                field_value = field_value.replace(tzinfo=None)

            elif isinstance(field_value, UUID):
                field_value = str(field_value)

            row[field.name] = field_value or ''
        rows.append(row)

    df = DataFrame(rows)
    wb = openpyxl.Workbook()
    ws = wb.active

    headers = [field.verbose_name for field in BimaCoreCountry._meta.fields]
    ws.append(headers)

    for r in df.iterrows():
        try:
            ws.append(list(r[1]))
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
