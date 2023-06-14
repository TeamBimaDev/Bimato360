from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BimaErpProductViewSet


router = DefaultRouter()
router.register('', BimaErpProductViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('export_csv',
         BimaErpProductViewSet.as_view({'get': 'export_data_csv'}),
         name='product-export_csv'),
    path('<str:public_id>/export_csv',
         BimaErpProductViewSet.as_view({'get': 'export_data_csv'}),
         name='product-export_csv'),

    path('export_pdf',
         BimaErpProductViewSet.as_view({'get': 'export_data_pdf'}),
         name='product-export_pdf'),
    path('<str:public_id>/export_pdf',
         BimaErpProductViewSet.as_view({'get': 'export_data_pdf'}),
         name='product-export_pdf'),

    path('export_xls',
         BimaErpProductViewSet.as_view({'get': 'export_xls'}),
         name='product-export_xls'),
    path('<str:public_id>/export_xls',
         BimaErpProductViewSet.as_view({'get': 'export_xls'}),
         name='product-export_xls'),
]
