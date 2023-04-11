from django.contrib import admin
from .models import BimaCorePoste
class BimaCorePosteAdmin(admin.ModelAdmin):
    list_display = ['name','description','requirements','responsibilities','department_id']
admin.site.register(BimaCorePoste,BimaCorePosteAdmin)