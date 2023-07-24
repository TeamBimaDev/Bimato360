import csv
import logging
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.http import HttpResponse
from pandas import DataFrame
import openpyxl
from io import BytesIO
from uuid import UUID
from datetime import datetime

from common.enums.company_type import get_company_type_choices
from common.enums.entity_status import get_entity_status_choices
from common.enums.gender import get_gender_choices
from common.enums.partner_type import get_partner_type_choices
from .models import BimaErpPartner

logger = logging.getLogger(__name__)


def generate_xls_file(queryset):
    rows = []
    for obj in queryset:
        try:
            row = {}
            for field in obj._meta.fields:
                try:
                    value = getattr(obj, field.name)

                    if field.choices:
                        value = getattr(obj, f"get_{field.name}_display")()

                    if isinstance(value, UUID):
                        value = str(value)

                    if isinstance(value, datetime):
                        value = value.replace(tzinfo=None)

                    row[field.name] = value
                except Exception as e:
                    logger.error(f"Error processing field {field.name} for object {obj.pk}: {e}")
            rows.append(row)
        except Exception as e:
            logger.error(f"Error processing object {obj.pk}: {e}")
            continue

    try:
        df = DataFrame(rows)

        wb = openpyxl.Workbook()
        ws = wb.active

        headers = [str(field.verbose_name) for field in BimaErpPartner._meta.fields]
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


CSV_TO_MODEL_MAP = {
    "partner_type": ["partner_type"],
    "company_type": ["company_type"],
    "name": ["first_name", "last_name"],
    "nom": ["first_name", "last_name"],
    "gender": ["gender"],
    "social_security_number": ["social_security_number"],
    "id_number": ["id_number"],
    "email": ["email"],
    "phone_number": ["phone"],
    "fax": ["fax"],
    "company_name": ["company_name"],
    "company_activity": ["company_activity"],
    "vat_id_number": ["vat_id_number"],
    "status": ["status"],
    "note": ["note"],
    "company_date_creation": ["company_date_creation"],
    "company_siren": ["company_siren"],
    "company_siret": ["company_siret"],
    "company_date_registration": ["company_date_registration"],
    "rcs_number": ["rcs_number"],
    "company_date_struck_off": ["company_date_struck_off"],
    "company_ape_text": ["company_ape_text"],
    "company_ape_code": ["company_ape_code"],
    "company_capital": ["company_capital"],
    "credit": ["credit"],
    "balance": ["balance"],
}

CHOICES_MAP = {
    "gender": get_gender_choices(),
    "partner_type": get_partner_type_choices(),
    "status": get_entity_status_choices(),
    "company_type": get_company_type_choices(),
}


def validate_choice_value(value: str, choices):
    choice_values = [item[0] for item in choices]
    if value not in choice_values:
        raise ValueError(f"Invalid value. Expected one of {choice_values}")
    return value


def create_partners_from_csv(file):
    error_rows = []
    partners = []

    csv_reader = csv.DictReader(file)

    for i, row in enumerate(csv_reader, start=1):
        partner_data = {}

        for csv_header, value in row.items():
            model_fields = CSV_TO_MODEL_MAP.get(csv_header.lower(), [])

            for model_field in model_fields:
                if model_field in ['gender', 'partner_type', 'status', 'company_type']:
                    choices = CHOICES_MAP[model_field]
                    try:
                        value = validate_choice_value(value, choices)
                    except ValueError as e:
                        error_rows.append({
                            'error': str(e),
                            'row': i,
                            'data': row
                        })
                        break
                partner_data[model_field] = value

        else:  # This else clause will run if no break statement was encountered in the for loop
            partner = BimaErpPartner(**partner_data)

            try:
                partner.full_clean()
                partners.append(partner)
            except ValidationError as e:
                error_rows.append({
                    'error': str(e),
                    'row': i,
                    'data': row
                })

    if partners:  # Only attempt to save partners if there are valid ones to save
        try:
            with transaction.atomic():
                BimaErpPartner.objects.bulk_create(partners)
        except IntegrityError as e:
            error_rows.append({
                'error': 'Bulk create operation failed: {}'.format(e),
                'row': 'N/A',
                'data': 'N/A'
            })

    return error_rows
