from django.db import transaction, IntegrityError

from .models import BimaCoreCurrency
from django.utils.translation import gettext_lazy as _


def import_data_from_csv_file(df):
    error_rows = []
    created_count = 0

    for index, row in df.iterrows():
        try:
            name = row.get('name')
            symbol = row.get('symbol')
            decimal_places = row.get('decimal_places')
            active = row.get('active', True)
            currency_unit_label = row.get('currency_unit_label')
            currency_subunit_label = row.get('currency_subunit_label')

            if not name:
                error_rows.append({'error': _('Name is missing'), _('data'): row.to_dict()})
                continue

            if not symbol:
                error_rows.append({'error': _('Symbol is missing'), _('data'): row.to_dict()})
                continue

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
                error_message = _('Currency with name {} already exists').format(name)
            elif 'symbol' in str(e):
                error_message = _('Currency with symbol {symbol} already exists').format(symbol)
            else:
                error_message = _('Integrity error occurred')

            error_rows.append({'error': error_message, _('data'): row.to_dict()})
        except Exception as e:
            error_rows.append({'error': str(e), _('data'): row.to_dict()})

    return error_rows, created_count
