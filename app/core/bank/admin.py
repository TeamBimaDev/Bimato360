from django.contrib import admin
from .models import BimaCoreBank
class BimaCoreBankAdmin(admin.ModelAdmin):
    list_display = ['name','street','street2','zip','city','state','country','email','active','bic']


admin.site.register(BimaCoreBank,BimaCoreBankAdmin)