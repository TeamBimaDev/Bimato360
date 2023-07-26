import csv

import pandas as pd
from django.db import transaction, IntegrityError
from django.db.models import Q, ForeignKey
from django.http import HttpResponse

from .models import BimaCoreCountry
from django.utils.translation import gettext_lazy as _

from core.currency.models import BimaCoreCurrency


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
                error_rows.append({'error': _('Name is missing'), 'data': row.to_dict()})
                continue
            if not code:
                error_rows.append({'error': _('Code is missing'), 'data': row.to_dict()})
                continue

            # Check if currency exists
            currency = BimaCoreCurrency.objects.filter(
                Q(name=currency_name_or_symbol) | Q(symbol=currency_name_or_symbol)).first()
            if not currency:
                error_rows.append(
                    {'error': _('Currency with name or symbol {} does not exist').format(currency_name_or_symbol),
                     'data': row.to_dict()})
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
                error_message = _('Country with name {} already exists').format(name)
            elif 'code' in str(e):
                error_message = _('Country with code {} already exists').format(code)
            else:
                error_message = _('Integrity error occurred')
            error_rows.append({'error': error_message, 'data': row.to_dict()})
        except Exception as e:
            error_rows.append({'error': str(e), 'data': row.to_dict()})

    return error_rows, created_count


def export_to_csv(queryset, model_fields):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    writer = csv.writer(response)

    field_names_to_show = [fd.name for fd in model_fields.fields if not isinstance(fd, ForeignKey)]
    related_fields_to_show = [fd.name for fd in model_fields.fields if isinstance(fd, ForeignKey)]

    writer.writerow(field_names_to_show + [f'{field}_name' for field in related_fields_to_show])

    for instance in queryset:
        row_data = [getattr(instance, field) if getattr(instance, field) is not None else '' for field in
                    field_names_to_show]
        related_data = [getattr(getattr(instance, field), 'name', '') if getattr(instance, field) is not None else ''
                        for field in related_fields_to_show]
        writer.writerow(row_data + related_data)

    return response
