from django.http import HttpResponse
from datetime import datetime
from uuid import UUID

from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
import tablib

import csv
from .models import BimaErpPartner

from common.enums.company_type import get_company_type_choices
from common.enums.entity_status import get_entity_status_choices
from common.enums.gender import get_gender_choices
from common.enums.partner_type import get_partner_type_choices

from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError


def generate_xls_file(data_to_export, model_fields):
    file_data = tablib.Dataset(headers=[fd.name for fd in model_fields.fields])

    for product in data_to_export:
        values = []
        for fd in model_fields.fields:
            value = None
            try:
                if fd.name in ['category', 'vat', 'unit_of_measure']:
                    value = getattr(getattr(product, fd.name), 'name', None)
                else:
                    value = getattr(product, fd.name, None)

                if isinstance(value, datetime):
                    value = value.replace(tzinfo=None)
                elif isinstance(value, UUID):
                    value = str(value)
            except Exception as e:
                print(f"Error while processing field {fd.name}: {e}")
            finally:
                values.append(value)
        file_data.append(values)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=data.xlsx'

    workbook = Workbook()
    sheet = workbook.active
    sheet.append(file_data.headers)

    header_font = Font(size=12, bold=True)
    for cell in sheet[1]:  # Assuming your header is in the first row
        cell.font = header_font

    # Write the data to the sheet
    for row_data in file_data:
        sheet.append(row_data)

    # Apply column width
    for column in range(1, len(file_data.headers) + 1):
        column_letter = get_column_letter(column)
        sheet.column_dimensions[column_letter].width = 12

    # Apply borders
    border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'),
                    bottom=Side(style='thin'))
    for row in sheet.iter_rows(min_row=1, max_row=sheet.max_row, min_col=1, max_col=sheet.max_column):
        for cell in row:
            cell.border = border

    quantity_index = file_data.headers.index('quantity')
    min_stock_level_index = file_data.headers.index('minimum_stock_level')
    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row,
                               min_col=quantity_index + 1,
                               max_col=quantity_index + 1):
        for cell in row:
            corresponding_min_stock_level_cell = sheet.cell(row=cell.row, column=min_stock_level_index + 1)
            if (cell.value is not None and corresponding_min_stock_level_cell.value is not None and
                    isinstance(cell.value, (float, int)) and isinstance(corresponding_min_stock_level_cell.value,
                                                                        (float, int)) and
                    cell.value <= corresponding_min_stock_level_cell.value):
                cell.fill = PatternFill(start_color='FFFF0000', end_color='FFFF0000',
                                        fill_type='solid')  # Red color
            else:
                cell.fill = PatternFill(start_color='FF00FF00', end_color='FF00FF00',
                                        fill_type='solid')  # Green color

    for column in sheet.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        sheet.column_dimensions[get_column_letter(column[0].column)].width = adjusted_width

    workbook.save(response)

    return response


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
