import csv
import logging

import pandas as pd
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


def import_partner_data_from_csv_file(df):
    error_rows = []
    created_count = 0

    for index, row in df.iterrows():
        try:
            # Load all the data from the row
            is_supplier = row.get('is_supplier') if isinstance(row.get('is_supplier'), bool) else False
            is_customer = row.get('is_customer') if isinstance(row.get('is_customer'), bool) else False
            partner_type = get_enum_value(PartnerType, str(row.get('partner_type')))
            company_type = get_enum_value(CompanyType, str(row.get('company_type')))

            first_name = str(row.get('first_name')) if pd.notnull(row.get('first_name')) else ""
            last_name = str(row.get('last_name')) if pd.notnull(row.get('last_name')) else ""
            gender = get_enum_value(Gender, str(row.get('gender')))

            social_security_number = str(row.get('social_security_number')) if pd.notnull(
                row.get('social_security_number')) else ""
            id_number = str(row.get('id_number')) if pd.notnull(row.get('id_number')) else ""
            email = str(row.get('email')) if pd.notnull(row.get('email')) else ""
            phone = str(row.get('phone')) if pd.notnull(row.get('phone')) else ""
            fax = str(row.get('fax')) if pd.notnull(row.get('fax')) else ""

            company_name = str(row.get('company_name')) if pd.notnull(row.get('company_name')) else ""
            company_activity = str(row.get('company_activity')) if pd.notnull(row.get('company_activity')) else ""
            vat_id_number = str(row.get('vat_id_number')) if pd.notnull(row.get('vat_id_number')) else ""

            status = get_enum_value(EntityStatus, str(row.get('status')))
            if status is None:
                status = 'ACTIVE'
            note = str(row.get('note')) if pd.notnull(row.get('note')) else ""

            company_date_creation = pd.to_datetime(row.get('company_date_creation'), errors='coerce') if pd.notnull(
                row.get('company_date_creation')) else None
            company_siren = str(row.get('company_siren')) if pd.notnull(row.get('company_siren')) else ""
            company_siret = str(row.get('company_siret')) if pd.notnull(row.get('company_siret')) else ""
            company_date_registration = pd.to_datetime(row.get('company_date_registration'),
                                                       errors='coerce') if pd.notnull(
                row.get('company_date_registration')) else None

            rcs_number = str(row.get('rcs_number')) if pd.notnull(row.get('rcs_number')) else ""
            company_date_struck_off = pd.to_datetime(row.get('company_date_struck_off'), errors='coerce') if pd.notnull(
                row.get('company_date_struck_off')) else None

            company_ape_text = str(row.get('company_ape_text')) if pd.notnull(row.get('company_ape_text')) else ""
            company_ape_code = str(row.get('company_ape_code')) if pd.notnull(row.get('company_ape_code')) else ""
            company_capital = str(row.get('company_capital')) if pd.notnull(row.get('company_capital')) else ""

            credit = row.get('credit') if isinstance(row.get('credit'), (int, float)) and pd.notnull(
                row.get('credit')) else 0
            balance = row.get('balance') if isinstance(row.get('balance'), (int, float)) and pd.notnull(
                row.get('balance')) else 0

            partner_type_name = get_enum_value(PartnerType, partner_type)
            handler = partner_handlers.get(partner_type_name)

            if not handler:
                continue

            error = handler(partner_type_name, first_name, company_type)

            if error is not None:
                error_rows.append(error)
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
                partner.full_clean()
                partner.save()
            created_count += 1
        except ValidationError as e:
            error_rows.append(
                {'error': _('Invalid data: {}').format(e), 'data': handle_error(partner_type, first_name)})
        except IntegrityError as e:
            error_message = _('Integrity error occurred: {}').format(str(e))
            error_rows.append({'error': str(error_message), 'data': handle_error(partner_type, first_name)})
        except Exception as e:
            error_rows.append({'error': str(e), 'data': handle_error(partner_type, first_name)})

    return error_rows, created_count


def export_to_csv(partners, model_fields):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="partners.csv"'
    field_names_to_show = [fd.name for fd in model_fields.fields]
    writer = csv.writer(response)
    writer.writerow(field_names_to_show)

    for partner in partners:
        row_data = []
        for field in field_names_to_show:
            try:
                value = getattr(partner, field)
                if hasattr(value, 'name'):
                    # This will handle foreign keys
                    value = getattr(value, 'name', None)
                elif field in ENUM_MAPPINGS:
                    # This will handle enums
                    enum_value = getattr(partner, field, None)
                    value = str(ENUM_MAPPINGS[field][enum_value].value) if enum_value is not None else None
                row_data.append(value if value is not None else '')
            except Exception as ex:
                pass
        writer.writerow(row_data)

    return response


def handle_individual(partner_type_name, first_name, optional=None):
    if not partner_type_name:
        return {'error': _('Partner Type does not exist'),
                'data': handle_error(partner_type_name, first_name)}
    return None


def handle_company(partner_type_name, first_name, company_type):
    if not partner_type_name or not company_type:
        return {'error': _('Partner Type or Company Type does not exist'),
                'data': handle_error(partner_type_name, first_name)}
    return None


partner_handlers = {
    PartnerType.INDIVIDUAL.name: handle_individual,
    PartnerType.COMPANY.name: handle_company,
}


def handle_error(partner_type, first_name):
    if partner_type is None:
        partner_type = "None"
    if first_name is None:
        first_name = "None"

    return partner_type + " " + first_name


def validate_choice_value(value: str, choices):
    choice_values = [item[0] for item in choices]
    if value not in choice_values:
        raise ValueError(f"Invalid value. Expected one of {choice_values}")
    return value


ENUM_MAPPINGS = {
    "partner_type": PartnerType,
    "gender": Gender,
    "status": EntityStatus,
    "company_type": CompanyType,
}
