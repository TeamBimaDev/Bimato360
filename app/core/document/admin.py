from django.contrib import admin
from .models import BimaCoreDocument


class BimaCoreDocumentAdmin(admin.ModelAdmin):
    list_display = ['document_name', 'description', 'file_name', 'file_extension',
                    'date_file', 'file_path', 'file_type']


admin.site.register(BimaCoreDocument, BimaCoreDocumentAdmin)
