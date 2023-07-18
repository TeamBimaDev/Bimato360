from django.db import transaction, IntegrityError
from django.db.models import Q

from .models import BimaCoreCountry
from django.utils.translation import gettext_lazy as _

from core.currency.models import BimaCoreCurrency


def import_data_from_csv_file(df):
    error_rows = []
    created_count = 0

    for index, row in df.iterrows():
        try:
            name = row.get('name')
            code = row.get('code')
            iso3 = row.get('iso3')
            iso2 = row.get('iso2')
            phone_code = row.get('phone_code')
            capital = row.get('capital')
            address_format = row.get('address_format')
            vat_label = row.get('vat_label')
            zip_required = row.get('zip_required', False)
            currency_name_or_symbol = row.get('currency')

            if not name:
                error_rows.append({'error': _('Name is missing'), 'data': row.to_dict()})
                continue

            if not code:
                error_rows.append({'error': _('Code is missing'), 'data': row.to_dict()})
                continue

            currency = BimaCoreCurrency.objects.filter(Q(name=currency_name_or_symbol) | Q(symbol=currency_name_or_symbol)).first()
            if not currency:
                error_rows.append({'error': _('Currency with name or symbol {} does not exist').format(currency_name_or_symbol), 'data': row.to_dict()})
                continue

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
                error_message = _('Country with code {code} already exists').format(code)
            else:
                error_message = _('Integrity error occurred')

            error_rows.append({'error': error_message, 'data': row.to_dict()})
        except Exception as e:
            error_rows.append({'error': str(e), 'data': row.to_dict()})

    return error_rows, created_count
