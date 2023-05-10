from django.contrib import admin
from .models import BimaCorePost
class BimaCorePostAdmin(admin.ModelAdmin):
    list_display = ['name','description','requirements','responsibilities','department_id']
admin.site.register(BimaCorePost,BimaCorePostAdmin)