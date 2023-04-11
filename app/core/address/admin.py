from django.contrib import admin
from .models import BimaCoreAddress
class BimaCoreAddressAdmin(admin.ModelAdmin):
    list_display = ['number','street','postal_code','city','parent_type']

admin.site.register(BimaCoreAddress, BimaCoreAddressAdmin)