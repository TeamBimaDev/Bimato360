from django.http import HttpResponse
from datetime import datetime
from uuid import UUID

from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
import tablib
import csv

from .models import BimaErpProduct


def generate_xls_file(data_to_export, model_fields):
    headers = [str(fd.verbose_name) for fd in model_fields.fields]
    file_data = tablib.Dataset()

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
            except Exception as ex:
                print(f"An error occurred while getting value of {fd.name}. Error: {str(ex)}")
            values.append(value)
        file_data.append(values)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=data.xlsx'

    workbook = Workbook()
    sheet = workbook.active

    # append headers
    sheet.append(headers)

    header_font = Font(size=12, bold=True)
    for cell in sheet[1]:
        cell.font = header_font

    for row_data in file_data:
        try:
            sheet.append(row_data)
        except ValueError as ex:
            print(ex)

    for column in range(1, len(headers) + 1):
        column_letter = get_column_letter(column)
        sheet.column_dimensions[column_letter].width = 12

    # Apply borders
    border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'),
                    bottom=Side(style='thin'))
    for row in sheet.iter_rows(min_row=1, max_row=sheet.max_row, min_col=1, max_col=sheet.max_column):
        for cell in row:
            cell.border = border

    quantity_index = headers.index(BimaErpProduct._meta.get_field('quantity').verbose_name)
    min_stock_level_index = headers.index(BimaErpProduct._meta.get_field('minimum_stock_level').verbose_name)
    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row,
                               min_col=quantity_index + 1,
                               max_col=quantity_index + 1):
        for cell in row:
            corresponding_min_stock_level_cell = sheet.cell(row=cell.row, column=min_stock_level_index + 1)
            if cell.value is not None and corresponding_min_stock_level_cell.value is not None and cell.value <= corresponding_min_stock_level_cell.value:
                cell.fill = PatternFill(start_color='FFFF0000', end_color='FFFF0000', fill_type='solid')  # Red color
            else:
                cell.fill = PatternFill(start_color='FF00FF00', end_color='FF00FF00', fill_type='solid')  # Green color

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


def export_to_csv(products, model_fields):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'
    field_names_to_show = [fd.name for fd in model_fields.fields]
    writer = csv.writer(response)
    writer.writerow(field_names_to_show)

    for product in products:
        writer.writerow([getattr(product, field) for field in field_names_to_show])

    return response
