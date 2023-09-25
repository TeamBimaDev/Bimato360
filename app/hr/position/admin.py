from django.contrib import admin

from .models import BimaHrPosition


class BimaHrPostAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'requirements', 'responsibilities', 'department_id']


admin.site.register(BimaHrPosition, BimaHrPostAdmin)
