from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
from uuid import UUID

from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
import tablib


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pdf_status = pisa.CreatePDF(html, dest=response)

    if pdf_status.err:
        return HttpResponse('Some errors were encountered <pre>' + html + '</pre>')

    return response


def generate_xls_file(data_to_export, model_fields):
    file_data = tablib.Dataset(headers=[fd.name for fd in model_fields.fields])

    for partner in data_to_export:
        values = []
        for fd in model_fields.fields:
            value = getattr(partner, fd.name)
            if isinstance(value, datetime):
                value = value.replace(tzinfo=None)
            elif isinstance(value, UUID):
                value = str(value)
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

    # Apply color based on is_supplier value
    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=file_data.headers.index('is_supplier') + 1,
                               max_col=file_data.headers.index('is_supplier') + 1):
        for cell in row:
            if cell.value:
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
