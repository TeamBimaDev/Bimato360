from django.contrib import admin
from .models import BimaCoreDepartment


class BimaCoreDepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


admin.site.register(BimaCoreDepartment, BimaCoreDepartmentAdmin)
