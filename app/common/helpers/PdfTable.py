from reportlab.platypus import Table, TableStyle
from django.apps import apps
from reportlab.lib import colors


class PdfTable:
    def __init__(self, model_name, fields):
        self.model_name = model_name
        self.fields = fields
        self.data = [fields]  # The fields are the header of the table

    def get_data(self):
        model = apps.get_model(app_label='core', model_name=self.model_name)
        items = model.objects.all()

        for item in items:
            row = [getattr(item, field) for field in self.fields]
            self.data.append(row)

    def create_table(self, data_chunk):
        table = Table(data_chunk)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        return table

    def chunks(self, lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
