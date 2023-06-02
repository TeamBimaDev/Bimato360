from django.contrib import admin
from .models import BimaCoreContact


class BimaCoreContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'fax', 'mobile', 'phone', 'parent_type']


admin.site.register(BimaCoreContact, BimaCoreContactAdmin)
