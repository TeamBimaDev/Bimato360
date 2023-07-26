import csv

import pandas as pd
from django.db import transaction, IntegrityError
from django.http import HttpResponse

from .models import BimaCoreCurrency
from django.utils.translation import gettext_lazy as _


def import_data_from_csv_file(df):
    error_rows = []
    created_count = 0

    for index, row in df.iterrows():
        try:
            name = str(row.get('name', '')) if pd.notna(row.get('name')) else ""
            symbol = str(row.get('symbol', '')) if pd.notna(row.get('symbol')) else ""
            decimal_places = int(row.get('decimal_places', 0)) if pd.notna(row.get('decimal_places')) else 0
            active = bool(row.get('active', True)) if pd.notna(row.get('active')) else True
            currency_unit_label = str(row.get('currency_unit_label', '')) if pd.notna(row.get('currency_unit_label')) else ""
            currency_subunit_label = str(row.get('currency_subunit_label', '')) if pd.notna(row.get('currency_subunit_label')) else ""

            if not name:
                error_rows.append({'error': _('Name is missing'), 'data': name if name else ""})
                continue
            if not symbol:
                error_rows.append({'error': _('Symbol is missing'), 'data': name if name else ""})
                continue

            # Create the object
            with transaction.atomic():
                BimaCoreCurrency.objects.create(
                    name=name,
                    symbol=symbol,
                    decimal_places=decimal_places,
                    active=active,
                    currency_unit_label=currency_unit_label,
                    currency_subunit_label=currency_subunit_label
                )
            created_count += 1
        except IntegrityError as e:
            if 'name' in str(e):
                error_message = _('Currency with name {} already exists').format(name if name else "")
            elif 'symbol' in str(e):
                error_message = _('Currency with symbol {} already exists').format(symbol if symbol else "")
            else:
                error_message = _('Integrity error occurred')
            error_rows.append({'error': error_message, 'data': name if name else ""})
        except Exception as e:
            error_rows.append({'error': str(e), 'data': name if name else ""})

    return error_rows, created_count


def export_to_csv(queryset, model_fields):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    writer = csv.writer(response)

    field_names_to_show = [fd.name for fd in model_fields.fields]
    writer.writerow(field_names_to_show)

    for instance in queryset:
        row_data = [getattr(instance, field) if getattr(instance, field) is not None else '' for field in field_names_to_show]
        writer.writerow(row_data)

    return response
