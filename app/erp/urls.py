<<<<<<< HEAD
from django.urls import path, include

app_name = 'erp'

urlpatterns = [
        path('partner/', include('erp.partner.urls')),
        path('category/', include('erp.category.urls')),
        path('unit_of_measure/', include('erp.unit_of_measure.urls')),
        path('vat/', include('erp.vat.urls')),
        path('product/', include('erp.product.urls')),
        path('sale_document/', include('erp.sale_document.urls')),
        path('purchase_document/', include('erp.purchase_document.urls')),
]
=======
from django.urls import path, include

app_name = 'erp'

urlpatterns = [
        path('partner/', include('erp.partner.urls')),
        path('category/', include('erp.category.urls')),
        path('unit_of_measure/', include('erp.unit_of_measure.urls')),
        path('vat/', include('erp.vat.urls')),
        path('product/', include('erp.product.urls')),
        path('sale_document/', include('erp.sale_document.urls')),
        path('purchase_document/', include('erp.purchase_document.urls')),
]
>>>>>>> origin/ma-branch
