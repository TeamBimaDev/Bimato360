from django.urls import path, include

app_name = 'erp'

urlpatterns = [
        path('partner/', include('erp.partner.urls')),
]
