from django.contrib import admin
from .models import BimaCoreCurrency


class BimaCoreCurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol', 'rounding', 'decimal_places', 'active',
                    'position', 'currency_unit_label', 'currency_subunit_label']


admin.site.register(BimaCoreCurrency, BimaCoreCurrencyAdmin)
