import csv
import logging
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from pandas import DataFrame
import openpyxl
from io import BytesIO
from uuid import UUID
from datetime import datetime

from common.enums.global_enum import get_enum_value
from .models import BimaErpPartner
from common.enums.company_type import CompanyType
from common.enums.entity_status import EntityStatus
from common.enums.gender import Gender
from common.enums.partner_type import PartnerType

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


def validate_choice_value(value: str, choices):
    choice_values = [item[0] for item in choices]
    if value not in choice_values:
        raise ValueError(f"Invalid value. Expected one of {choice_values}")
    return value


def import_partner_data_from_csv_file(df):
    error_rows = []
    created_count = 0

    for index, row in df.iterrows():
        try:
            # Load all the data from the row
            is_supplier = row.get('is_supplier')
            is_customer = row.get('is_customer')
            partner_type = get_enum_value(PartnerType, row.get('partner_type'))
            company_type = get_enum_value(CompanyType, row.get('company_type'))
            first_name = row.get('first_name')
            last_name = row.get('last_name')
            gender = get_enum_value(Gender, row.get('gender'))
            social_security_number = row.get('social_security_number')
            id_number = row.get('id_number')
            email = row.get('email')
            phone = row.get('phone')
            fax = row.get('fax')
            company_name = row.get('company_name')
            company_activity = row.get('company_activity')
            vat_id_number = row.get('vat_id_number')
            status = get_enum_value(EntityStatus, row.get('status'))
            note = row.get('note')
            company_date_creation = row.get('company_date_creation')
            company_siren = row.get('company_siren')
            company_siret = row.get('company_siret')
            company_date_registration = row.get('company_date_registration')
            rcs_number = row.get('rcs_number')
            company_date_struck_off = row.get('company_date_struck_off')
            company_ape_text = row.get('company_ape_text')
            company_ape_code = row.get('company_ape_code')
            company_capital = row.get('company_capital')
            credit = row.get('credit')
            balance = row.get('balance')

            if not partner_type or not status or not company_type:
                error_rows.append(
                    {'error': _('Partner Type, Status, or Company Type does not exist'), 'data': row.to_dict()})
                continue

            with transaction.atomic():
                partner = BimaErpPartner(
                    is_supplier=is_supplier,
                    is_customer=is_customer,
                    partner_type=partner_type,
                    company_type=company_type,
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    social_security_number=social_security_number,
                    id_number=id_number,
                    email=email,
                    phone=phone,
                    fax=fax,
                    company_name=company_name,
                    company_activity=company_activity,
                    vat_id_number=vat_id_number,
                    status=status,
                    note=note,
                    company_date_creation=company_date_creation,
                    company_siren=company_siren,
                    company_siret=company_siret,
                    company_date_registration=company_date_registration,
                    rcs_number=rcs_number,
                    company_date_struck_off=company_date_struck_off,
                    company_ape_text=company_ape_text,
                    company_ape_code=company_ape_code,
                    company_capital=company_capital,
                    credit=credit,
                    balance=balance
                )
                partner.full_clean()  # Validate the model instance
                partner.save()
            created_count += 1
        except ValidationError as e:
            error_rows.append({'error': _('Invalid data: {}').format(e), 'data': row.to_dict()})
        except IntegrityError as e:
            error_message = _('Integrity error occurred: {}').format(str(e))
            error_rows.append({'error': str(error_message), 'data': row.to_dict()})
        except Exception as e:
            error_rows.append({'error': str(e), 'data': row.to_dict()})

    return error_rows, created_count


ENUM_MAPPINGS = {
    "partner_type": PartnerType,
    "gender": Gender,
    "status": EntityStatus,
    "company_type": CompanyType,
}


def export_to_csv(partners, model_fields):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="partners.csv"'
    field_names_to_show = [fd.name for fd in model_fields.fields]
    writer = csv.writer(response)
    writer.writerow(field_names_to_show)

    for partner in partners:
        row_data = []
        for field in field_names_to_show:
            value = getattr(partner, field)
            if hasattr(value, 'name'):
                # This will handle foreign keys
                value = getattr(value, 'name', None)
            elif field in ENUM_MAPPINGS:
                # This will handle enums
                enum_value = getattr(partner, field, None)
                value = ENUM_MAPPINGS[field][enum_value].value if enum_value is not None else None
            row_data.append(value if value is not None else '')
        writer.writerow(row_data)

    return response
